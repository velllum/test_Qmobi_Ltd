# import codecs
# import json
# import socketserver
# from http.server import HTTPServer, BaseHTTPRequestHandler
#
#
# class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
#
#
#     dic = {
#         "валюта": "654654654",
#         "запрошенное значение": 50,
#         "результирующее значение": 250,
#     }
#
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#
#     def do_GET(self):
#         self._set_headers()
#
#         text = json.dumps(self.dic, sort_keys=True, indent=4)
#
#         text = codecs.decode(text, 'unicode_escape')
#
#         print(self.dic)
#
#         print(self.path)
#
#         self.wfile.write(bytes(text, "utf8"))
#
#
#
#
#
#
#     def do_POST(self):
#         self._set_headers()
#
#         self.cgi_directories = ['/', '/cgi-bin', '/htbin', '/hello.py']
#
#         content_length = int(self.headers['Content-Length'])
#
#         text = self.rfile.read(content_length)
#
#         print(text.decode("utf8"))
#         text_ = text.decode("utf8")
#         print(dict(json.loads(text_)))
#
#         post_dic = dict(json.loads(text_))
#
#         self.dic["валюта"] = post_dic["валюта"]
#
#         self.wfile.write(text)
#
#         print(self.dic)
#
#
#
#
# httpd = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
# print("сервер работает")
# httpd.serve_forever()


#!/usr/bin/env python3
"""
Very simple HTTP server in python for logging requests
Usage::
    ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()