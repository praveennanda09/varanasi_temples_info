#!/usr/bin/env python3
"""
Zero-dependency local offline web server for Kashi Offline Website Archive.
Runs on any system with Python 3 (Desktop, Laptop, or Android via Termux).
Does not require any internet connection.
"""
import http.server
import socketserver
import os
import webbrowser
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("=" * 60)
        print("  KASHI OFFLINE WEBSITE ARCHIVE LOCAL SERVER")
        print("=" * 60)
        print(f"  Server running locally at: {url}")
        print("  Offline Guide Master Index: http://localhost:8080/../Kashi_Pilgrimage_Master_Index.html")
        print("  No internet connection required.")
        print("  Press Ctrl+C to stop the server.")
        print("=" * 60)
        try:
            webbrowser.open(url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    run()
