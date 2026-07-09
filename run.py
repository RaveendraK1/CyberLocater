import http.server
import socketserver
import webbrowser
import os
import urllib.parse
import urllib.request
import subprocess
import json

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Custom API Route for Traceroute
        if parsed_path.path == '/api/traceroute':
            query = urllib.parse.parse_qs(parsed_path.query)
            ip = query.get('ip', [''])[0]
            if ip:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Execute tracert with max 15 hops, no DNS (-d), and 500ms timeout per hop (-w 500)
                try:
                    result = subprocess.run(['tracert', '-d', '-h', '15', '-w', '500', ip], capture_output=True, text=True, timeout=30)
                    output = result.stdout if result.stdout else result.stderr
                except subprocess.TimeoutExpired as e:
                    partial = e.stdout if e.stdout else ""
                    output = partial + "\n\n[!] Traceroute stopped: Reached maximum time limit (30s) or firewall blocked further hops."
                except Exception as e:
                    output = f"Error: {str(e)}"
                
                self.wfile.write(json.dumps({'contents': output}).encode('utf-8'))
                return
            else:
                self.send_response(400)
                self.end_headers()
                return
                
        # Custom API Route for WHOIS
        if parsed_path.path == '/api/whois':
            query = urllib.parse.parse_qs(parsed_path.query)
            ip = query.get('ip', [''])[0]
            if ip:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                try:
                    import socket
                    def query_server(server, query_ip):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(10)
                        s.connect((server, 43))
                        s.send((query_ip + "\r\n").encode())
                        res = b""
                        while True:
                            d = s.recv(4096)
                            if not d: break
                            res += d
                        s.close()
                        return res.decode(errors='replace')

                    # Start at IANA
                    iana_res = query_server("whois.iana.org", ip)
                    refer = None
                    for line in iana_res.split('\n'):
                        if line.lower().startswith('refer:'):
                            refer = line.split(':', 1)[1].strip()
                            break
                            
                    if refer:
                        whois_data = query_server(refer, ip)
                    else:
                        whois_data = iana_res
                        
                    output = {'success': True, 'data': whois_data}
                except Exception as e:
                    output = {'success': False, 'error': str(e)}
                
                self.wfile.write(json.dumps(output).encode('utf-8'))
                return
            else:
                self.send_response(400)
                self.end_headers()
                return
        
        # Serve normal static files
        super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)

        # Custom API Route: AI Threat Analyst (powered by Mesh API)
        if parsed_path.path == '/api/analyze':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                payload = json.loads(body.decode('utf-8'))
            except Exception:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': 'Invalid JSON body'}).encode('utf-8'))
                return

            ip = payload.get('ip', 'unknown')
            country = payload.get('country', 'unknown')
            isp = payload.get('isp', 'unknown')
            asn = payload.get('asn', 'unknown')
            timezone = payload.get('timezone', 'unknown')
            is_proxy = payload.get('isProxy', False)
            is_hosting = payload.get('isHosting', False)
            lang = payload.get('lang', 'en')  # 'en' or 'hi' (Bharat-track Hindi toggle)

            lang_instruction = (
                "Respond entirely in Hindi (Devanagari script)."
                if lang == 'hi' else
                "Respond in English."
            )

            prompt = f"""You are a cybersecurity threat analyst reviewing OSINT data for an IP address.

IP: {ip}
Country: {country}
ISP/Org: {isp}
ASN: {asn}
Timezone: {timezone}
Proxy/VPN detected: {is_proxy}
Datacenter/Hosting IP: {is_hosting}

{lang_instruction}

Return ONLY valid JSON (no markdown, no code fences) in this exact shape:
{{
  "riskSummary": "2-3 sentence plain-English risk explanation",
  "keyFlags": ["short flag 1", "short flag 2"],
  "recommendedAction": "one short sentence: monitor / investigate further / block"
}}"""

            mesh_api_key = os.environ.get('MESH_API_KEY')

            if not mesh_api_key:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': 'MESH_API_KEY not set on server'
                }).encode('utf-8'))
                return

            try:
                mesh_body = json.dumps({
                    "model": "openai/gpt-4o-mini",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }).encode('utf-8')

                req = urllib.request.Request(
                    "https://api.meshapi.ai/v1/chat/completions",
                    data=mesh_body,
                    headers={
                        "Authorization": f"Bearer {mesh_api_key}",
                        "Content-Type": "application/json"
                    },
                    method="POST"
                )

                with urllib.request.urlopen(req, timeout=20) as resp:
                    mesh_response = json.loads(resp.read().decode('utf-8'))

                raw_text = mesh_response['choices'][0]['message']['content']

                # Strip accidental markdown code fences if the model adds them
                clean_text = raw_text.strip()
                if clean_text.startswith('```'):
                    clean_text = clean_text.split('```')[1]
                    if clean_text.startswith('json'):
                        clean_text = clean_text[4:]
                    clean_text = clean_text.strip()

                analysis = json.loads(clean_text)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'data': analysis}).encode('utf-8'))

            except Exception as e:
                self.send_response(200)  # 200 so frontend can show a graceful fallback
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'error': f'Mesh API call failed: {str(e)}'
                }).encode('utf-8'))

            return
        else:
            self.send_response(404)
            self.end_headers()
            return

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"CyberLocator is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down CyberLocator...")
