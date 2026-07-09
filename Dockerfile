FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install any Python dependencies (none required for the current code, but keep placeholder)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; else echo "No requirements.txt or empty, skipping pip install."; fi

# Expose the port (Render provides PORT env var, default to 8000)
EXPOSE 8000

# Ensure the server listens on all interfaces (run.py already does this)
CMD ["python", "run.py"]

