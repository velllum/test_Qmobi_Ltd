#  # from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # python2
# from http.server import BaseHTTPRequestHandler, HTTPServer # python3
# class HandleRequests(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'text/html')
#         self.end_headers()
#
#     def do_GET(self):
#         self._set_headers()
#         self.wfile.write("received get request")
#
#     def do_POST(self):
#         '''Reads post request body'''
#         self._set_headers()
#         content_len = int(self.headers['Content-Length'])
#         post_body = self.rfile.read(content_len)
#         self.wfile.write("received post request:<br>{}".format(post_body))
#
#     def do_PUT(self):
#         self.do_POST()
#
# host = ''
# port = 80
# HTTPServer((host, port), HandleRequests).serve_forever()


from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO


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
        print(response.getvalue())
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()
