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

print("Host:\t"+host_name)
print("Port:\t"+port_name)
print("Path:\t"+path_name)
# ______________________________________________________________________________________________
# host_name = 'httpbin.org'
# port_name = '80'


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

request = "GET %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\n\r\n" \
          %("/", host_name, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir")

print(request)

try:
    s.sendall(request.encode())
    # print(request.status_code)
except socket.error:
    print('Send failed')
    sys.exit()

print('# Receive data from server')
reply = str(s.recv(4096), 'utf-8')

print(reply)

# data = b''
# while True:
#     buf = s.recv(1024)
#     if not buf:
#         break
#     data += buf
# print(data)

def regex(s, tag):
    text = re.findall("<" +tag+ ">(.*?)</" +tag+ ">", s, re.DOTALL)
    text = str(text).replace("[", "")
    text = str(text).replace("]", "")
    text = str(text).replace("'", "")
    text = str(text).split(" ")
    for i in text:
        if i == "":
            text.remove(i)
    return text

def link(s):
    text = re.findall("<a href=(.*?)>.*?</a>", s, re.DOTALL)
    text = str(text).replace("[", "")
    text = str(text).replace("]", "")
    text = str(text).replace("'", "")
    text = str(text).replace("\"", "")
    text = str(text).split(" ")
    for i in text:
        if i == "":
            text.remove(i)
    return text

def string(s):
    text = ""
    for i in s:
        text += str(i) + " "
    return text

def access_code(s):
    access_code = ""
    for i in regex(s, "title"):
        if str(i).isdigit():
            access_code = str(i)
    return access_code

# if int(access_code(reply)) > 299 and int(access_code(reply)) < 400:
#     print("The response code: " + access_code(reply))
#     print("The URL where the file is located: " + string(link(reply)))

x = requests.get("https://"+host_name+path_name, params={'Host': host_name, 'Time': str(datetime.datetime.now()), 'Class-name': 'VCU-CMSC440-2022', 'User-name': 'Masrik Dahir'})
print(x.headers)