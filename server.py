#!/usr/bin/env python3
"""
Simple HTTP server for serving the Cognition Task Dashboard.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/':
            self.path = '/dashboard.html'
        return super().do_GET()

def main():
    port = 8080
    
    try:
        with socketserver.TCPServer(("", port), DashboardHandler) as httpd:
            print(f"Cognition Task Dashboard server starting...")
            print(f"Server running at http://localhost:{port}")
            print(f"Access the dashboard at http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except OSError as e:
        if e.errno == 48:
            print(f"Port {port} is already in use. Please try a different port.")
        else:
            print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
