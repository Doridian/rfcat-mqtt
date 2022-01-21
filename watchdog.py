from http.server import BaseHTTPRequestHandler
import socketserver
from time import monotonic

PORT = 8080

ok_until = 0
period = 0

class ReadyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ok = monotonic() <= ok_until
        self.send_response(204 if ok else 400)
        self.end_headers()

def serve():
    with socketserver.TCPServer(("", PORT), ReadyHTTPRequestHandler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def watchdog_ping():
    global ok_until
    ok_until = monotonic() + period

def set_watchdog_period(set_period):
    global period
    period = set_period
