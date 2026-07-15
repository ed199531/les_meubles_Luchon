#!/usr/bin/env python3
"""Serveur statique local pour Les Meublés de Luchon.
Sert le dossier /site sur le port 8137 avec des URLs propres (index.html de dossier).
"""
import http.server
import socketserver
import functools
import os

PORT = 8137
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")


class Handler(http.server.SimpleHTTPRequestHandler):
    # Empêche la mise en cache pendant le développement + entêtes de sécurité de démo
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        super().end_headers()


if __name__ == "__main__":
    handler = functools.partial(Handler, directory=BASE)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Les Meublés de Luchon — http://localhost:{PORT}  (dossier: {BASE})")
        httpd.serve_forever()
