#!/usr/bin/env python3
"""
Zero-dependency local offline web server for the Kashi Offline Pilgrimage Guide Pack.
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
        master_url = f"http://localhost:{PORT}/Kashi_Pilgrimage_Master_Index.html"
        mirror_url = f"http://localhost:{PORT}/Kashi_Exact_Offline_Website/index.html"
        print("=" * 65)
        print("    KASHI OFFLINE PILGRIMAGE ARCHIVE & KNOWLEDGE BASE")
        print("=" * 65)
        print("  Status: 100% Offline (No Internet Connection Required)")
        print(f"  Curated Master Portal: {master_url}")
        print(f"  Exact Website Mirror:  {mirror_url}")
        print("  Press Ctrl+C to stop the server.")
        print("=" * 65)
        try:
            webbrowser.open(master_url)
        except Exception:
            pass
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    run()
