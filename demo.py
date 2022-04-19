# #!/usr/bin/env python
#
# import argparse
# import http.server
# import os
#
# class HTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_PUT(self):
#         path = self.translate_path(self.path)
#         if path.endswith('/'):
#             self.send_response(405, "Method Not Allowed")
#             self.wfile.write("PUT not allowed on a directory\n".encode())
#             return
#         else:
#             try:
#                 os.makedirs(os.path.dirname(path))
#             except FileExistsError: pass
#             print(self.headers['Content-Length'])
#             length = int(self.headers['Content-Length'])
#             with open(path, 'wb') as f:
#                 f.write(self.rfile.read(length))
#             self.send_response(201, "Created")
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--bind', '-b', default='127.0.0.1', metavar='ADDRESS',
#                         help='Specify alternate bind address '
#                              '[default: all interfaces]')
#     parser.add_argument('port', action='store',
#                         default=8000, type=int,
#                         nargs='?',
#                         help='Specify alternate port [default: 8000]')
#     args = parser.parse_args()
#
#     http.server.test(HandlerClass=HTTPRequestHandler, port=args.port, bind=args.bind)
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv

BIND_HOST = 'localhost'
PORT = 8000


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.write_response(b'')

    def do_POST(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        print(body)


    def do_PUT(self):
        content_length = int(self.headers.get('content-length', 0))
        body = self.rfile.read(content_length)
        print(body)
        self.write_response(body)
        print(self.path)
        lines = ""
        with open(str(self.path)) as f:
            lines = f.read()
        print(lines)

        directory = './HTTPServer_html/'
        filename = str(self.path)
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        file.write(lines)
        file.close()

    def write_response(self, content):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(content)

        print(self.headers)
        print(content.decode('utf-8'))


if len(argv) > 1:
    arg = argv[1].split(':')
    BIND_HOST = arg[0]
    PORT = int(arg[1])

print(f'Listening on http://{BIND_HOST}:{PORT}\n')

httpd = HTTPServer((BIND_HOST, PORT), SimpleHTTPRequestHandler)
httpd.serve_forever()