# Author: Masrik Dahir
# Date: 2021-05-04
import datetime
import os
import socket
import sys
import re

def html(st:str):
    arg = st.split('<!DOCTYPE')[1]
    arg = '<!DOCTYPE' + arg
    return arg

def regex(s, tag):
    text = re.findall("<" + tag + ">(.*?)</" + tag + ">", s, re.DOTALL)
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

def string(s, diff=" "):
    text = ""
    for i in s:
        text += diff + str(i)
    return text

def access_code(s):
    access_code = ""
    for i in regex(s, "title"):
        if str(i).isdigit():
            access_code = str(i)
    return access_code

def tag(st: str, start, end, included=True):
    new = st.split(start)[1:]
    new = string(new)
    new_2 = new.split(end)[0]
    return str(start) + str(new_2) + str(end)

input = ""
for i in sys.argv:
    if "http" in str(i):
        input = i

host_name = ""
port_name = ""
path_name = ""
file_name = ""

if input[0:7] != 'http://':
    sys.exit("ERR -arg 1")
# parse the url into hostname, port, and path
else:
    host_name = input.split("/")[2]
    host_name = re.sub(":\w*", "", host_name)
    host_name = re.sub("\\\\\w*", "", host_name)

    if len(input.split(":")) == 3:
        # print(str(input))
        port_name = input.split("/")[2].split(":")[1]

    if len(input.split("/")) >= 4:
        path_name = string(input.split("/")[3:], "/")

    if port_name == "":
        port_name = "80"

    if path_name == "":
        path_name = "/"

print("Host:\t" + host_name)
print("Port:\t" + port_name)
print("Path:\t" + str(path_name))
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
    remote_ip = socket.gethostbyname(host_name)
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()
try:
    print('# Connecting to server, ' + host_name + ' (' + remote_ip + ')')
    s.connect((remote_ip, int(port_name)))
    print()
except:
    sys.exit("The host name or the port number is incorrect.\n")

def send():
    if len(sys.argv) == 2:
        print('# Sending data to server')
        request = "GET %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\n\r\n" \
                  % (path_name, host_name, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir")

        print(request)

        try:
            s.sendall(request.encode('utf-8'))
            # print(request.status_code)
        except socket.error:
            sys.exit('Send failed')

        print('# Receive data from server')
        reply = s.recvfrom(2048)
        print(reply[0].decode('utf-8'))
        # status_code = int(str(reply).split("\n")[0].split(' ')[1])
        #
        # if status_code >= 200 and status_code < 300:
        #
        #     print("Response code: %s" %(status_code))
        #
        #     if path_name == '/':
        #         file_name = "index.html"
        #     else:
        #         file_name = path_name.split('/')[-1]
        #     cwd = os.getcwd()
        #     print(cwd)
        #     open(format(cwd) + "/" + file_name, "w").write(html(reply[0].decode('utf-8')))



    if len(sys.argv) == 4:
        file_name = sys.argv[3]
        print("File:\t" + file_name)
        print('# Sending data to server')
        request = "PUT %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\nfiles: %s\r\n\r\n" \
                  % (file_name, host_name, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir", file_name)

        print(request)

        try:
            s.sendall(request.encode('utf-8'))
            # print(request.status_code)
        except socket.error:
            print('Send failed')
            sys.exit()

        print('# Receive data from server')
        reply = s.recvfrom(2048)
        print(reply[0].decode())

try:
    send()
except KeyboardInterrupt:
    pass
