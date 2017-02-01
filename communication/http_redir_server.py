__author__ = 'oshmuel'

"""
URL redirection example.

reference:
https://wiki.python.org/moin/BaseHttpServer
"""

import BaseHTTPServer
import time
import sys
import socket

MSG_FORMAT = "<html><head></head><body><h1>Response!! {token}</h1><div><p>this is a response</p></div></body></html>"

HOST_NAME = 'localhost' if len(sys.argv) < 2 else sys.argv[1]
PORT_NUMBER = 48888 if len(sys.argv) < 2 else int(sys.argv[2])
MODE = "simple" if len(sys.argv) < 2 else sys.argv[3]
MSG = MSG_FORMAT.format(token=str(HOST_NAME) + ":" + str(PORT_NUMBER) ) if len(sys.argv) < 5 else MSG_FORMAT.format(token=sys.argv[4])

class RedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(302)
        s.send_header("Location", 'http://localhost:33333/manual.pdf')
        s.end_headers()

    def do_GET(s):
        s.do_HEAD()

class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(s):
        message = MSG
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(message)

class MarkedHttpServer(BaseHTTPServer.HTTPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_IP, 19, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, 36, 3)
        self.socket.setsockopt(socket.SOL_TCP, socket.TCP_MAXSEG, 1300)

        BaseHTTPServer.HTTPServer.server_bind(self)

if __name__ == '__main__':
    print sys.argv
    server_class = BaseHTTPServer.HTTPServer

    if MODE == "simple":
        server_class = BaseHTTPServer.HTTPServer 
        handler = SimpleHandler
    if MODE == "simple_marked":
        server_class = MarkedHttpServer 
        handler = SimpleHandler
    elif MODE == "redirectr":
        handler = RedirectHandler

    httpd = server_class((HOST_NAME, PORT_NUMBER), handler)

    print "options: ", str(httpd.socket.getsockopt(socket.SOL_SOCKET, 36))

    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
