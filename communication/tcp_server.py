#!/usr/bin/env python

import socket

IP_TRANSPARENT = 19
SO_MARK = 36


TCP_IP = '127.0.0.1'
TCP_PORT = 62057 #6666
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_IP, IP_TRANSPARENT, 1)
s.setsockopt(socket.SOL_SOCKET, SO_MARK, 3)

s.bind((TCP_IP, TCP_PORT))
s.listen(100)

conn, addr = s.accept()

print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    conn.send(data)  # echo
conn.close()
