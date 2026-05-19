"""Simple reverse proxy to bypass localtunnel interstitial page."""
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

TUNNEL_URL = "https://fapai3.loca.lt"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        target = TUNNEL_URL + self.path
        req = urllib.request.Request(
            target,
            headers={
                "bypass-tunnel-reminder": "true",
                "User-Agent": "Mozilla/5.0 (compatible; ProxyServer/1.0)"
            }
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                ct = resp.headers.get("Content-Type", "text/html")
                self.send_response(200)
                self.send_header("Content-Type", ct)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(str(e).encode())

if __name__ == "__main__":
    port = 8888
    server = HTTPServer(("0.0.0.0", port), ProxyHandler)
    print(f"Proxy running on http://localhost:{port}")
    server.serve_forever()
