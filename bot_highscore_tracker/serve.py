#!/usr/bin/env python3
"""
Simple HTTP server to serve the frontend with player data.
Run: python serve.py
Then open: http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

def main():
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"🚀 Server running at {url}")
        print(f"📁 Serving from: {script_dir}")
        print(f"\nPress Ctrl+C to stop the server")
        
        # Try to open browser
        try:
            webbrowser.open(url)
            print(f"🌐 Opening browser...")
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Server stopped.")

if __name__ == "__main__":
    main()
