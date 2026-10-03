"""Serveur LAN autonome avec ressources locales et API sans état."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from .model import simulate
from .economics import calculate, bridge
from .pedagogy import catalog

STATIC = Path(__file__).parent / 'static'
ASSETS = {'/': ('lab.html', 'text/html; charset=utf-8'),
          '/ws-ps': ('index.html', 'text/html; charset=utf-8'),
          '/lab.js': ('lab.js', 'text/javascript; charset=utf-8'),
          '/plots.js': ('plots.js', 'text/javascript; charset=utf-8'),
          '/lab.css': ('lab.css', 'text/css; charset=utf-8'),
          '/app.js': ('app.js', 'text/javascript; charset=utf-8'),
          '/style.css': ('style.css', 'text/css; charset=utf-8')}

class Handler(BaseHTTPRequestHandler):
    def send(self, status, data, content_type='application/json; charset=utf-8'):
        body = json.dumps(data, allow_nan=False).encode() if isinstance(data, dict) else data
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == '/api/catalog':
            return self.send(200, catalog())
        if path == '/health':
            return self.send(200, {'status': 'ok'})
        if path not in ASSETS:
            return self.send(404, {'error': 'Page introuvable.'})
        name, mime = ASSETS[path]
        self.send(200, (STATIC / name).read_bytes(), mime)

    def do_POST(self):
        endpoints = {'/api/simulate': simulate, '/api/lab': calculate, '/api/bridge': bridge}
        if self.path not in endpoints:
            return self.send(404, {'error': 'Route inconnue.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 16384:
                raise ValueError('Taille de requête invalide.')
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError('Objet JSON attendu.')
            self.send(200, endpoints[self.path](payload))
        except (ValueError, TypeError, OverflowError) as exc:
            self.send(400, {'error': str(exc)})

if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0', int(os.environ.get('PORT', '8000'))), Handler).serve_forever()
