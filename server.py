# # server.py
# import http.server # Our http server handler for http requests
# import socketserver # Establish the TCP Socket connections
#
# PORT = 9000
#
# class GetHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         self.path = '/api/index.html'
#         print(self.path)
#         return http.server.SimpleHTTPRequestHandler.do_GET(self)
#
#     # def do_POST(self):
#     #     self.path = 'index.html'
#     #     return http.server.SimpleHTTPRequestHandler.do_POST(self)
# #
# class PostHttpRequestHandler(http.server.CGIHTTPRequestHandler):
#     def do_POST(self):
#         self.path = 'index.html'
#         return http.server.CGIHTTPRequestHandler.do_POST(self)
#
#
#
# Handler = GetHttpRequestHandler
#
#
# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("Http Server Serving at port", PORT)
#     httpd.serve_forever()