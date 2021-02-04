#!/usr/bin/env python3
print("Content-Type: text/html\n")
print("<!doctype html><title>Hello</title><h2>hello world</h2>")

from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO

import cgi


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        print(self.server)
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        print(response.getvalue(), body)
        self.wfile.write(response.getvalue())



httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()