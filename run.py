import http.server
import socketserver
import webbrowser
import os
import urllib.parse
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

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"CyberLocator is running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down CyberLocator...")
