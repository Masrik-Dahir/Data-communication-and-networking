# Author: Masrik Dahir
# Date: 2021-05-04
import datetime
import socket
import requests
import sys
import re


input = str(sys.argv[1])
addSlash = False
p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*)(?P<path>[^\s]*)'
link = re.search(p,input)

host_name = link.group('host')

port_name = link.group('port')
if port_name == "":
    port_name = "80"
    addSlash = True

path_name = link.group('path')
if addSlash:
    path_name = "/"+path_name
if path_name == "":
    path_name = "/"
# ______________________________________________________________________________________________




print('# Creating socket')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('# Getting remote IP address')
try:
    remote_ip = socket.gethostbyname( host_name )
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()
print('# Connecting to server, ' + host_name + ' (' + remote_ip + ')')
s.connect((remote_ip , int(port_name)))
print('# Sending data to server')

request = "GET / HTTP/1.0\r\n\r\n"

print(request)

try:
    s.sendall(request.encode())
    # print(request.status_code)
except socket.error:
    print('Send failed')
    sys.exit()

print('# Receive data from server')
reply = str(s.recv(4096)).split(';')

for i in reply:
    print(i)

