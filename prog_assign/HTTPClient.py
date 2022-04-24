# ----------------------------------------------------
#  Masrik Dahir
#  Date: 04/24/2022
#
#  ---------------------------------------------------
#  Usage Guide
#  (1)  Valid GET request
#       (a) python HTTPClient.py http://172.18.233.74:10004/HTML/index.html
#       (b) python HTTPClient.py http://172.18.233.74:10004
#       (c) python HTTPClient.py http://egr.vcu.edu
#       (d) python HTTPClient.py http://www.testingmcafeesites.com/
#
#  (2)  Invalid GET request
#       (a) python HTTPClient.py http://172.18.233.74:10004/inx
#       (b) python HTTPClient.py https://egr.vcu.edu
#       (c) python HTTPClient.py http://engr.vcu.edu
#       (d) python HTTPClient.py http://egr.vcu.edu/dsadsa
#       (e) python HTTPClient.py http://172.18.233.74:10004 index.html
#       (f) python HTTPClient.py http://nonwe:10004 index.html
#       (g) python HTTPClient.py http://172.18.233.74:-34 index.html wwew
#
#  (3)  Valid PUT request
#       (a) python PUT HTTPClient.py http://172.18.233.74:10004 HTTP/index.html
#       (b) python PUT HTTPClient.py http://172.18.233.74:10004 index.html
#
#  (4)  Invalid PUT request
#       (a) python PUT HTTPClient.py http://172.18.233.74:10004/sdfsdsd
#       (b) python PUT HTTPClient.py http://172.18.233.74:10004 dasdsad
#       (c) python PUT HTTPClient.py http://172.18.233.74:10004 HTTP/index.html fdsfdsf
#       (d) python PUT HTTPClient.py http://172.18.233.74:10004 HTTP/index.html fdsfdsf
#       (e) python PUT HTTPClient.py http://172.18.233.74:4234324324324 index.html
#       (f) python PUT HTTPClient.py http://172.18.233.74:-34 index.html
#
#
# ----------------------------------------------------

# imports
import datetime
import os
import socket
import sys
import re
import webbrowser


# html function parse teh html code from the server response
def html(st):
    arg = st.split('<!DOCTYPE')[1]
    arg = '<!DOCTYPE' + arg
    return arg


# semicolon function finds the phrases after semicolon of a an attribute i.e. "Host: egr.vcu.edu" --> "egr.vcu.edu"
def semicolon(st, var):
    arg = string(re.findall("(?<=%s:).*" % (var), st))
    arg = re.sub("^\s+", "", arg)
    return arg


# regex finds text between a same tag
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


# link finds the link on <a href="#link"> ... </a> tag in html
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


# string converts a list to string with a preffered seperator
# string(["a", "b", "c"], " ") --> "a b c"
def string(s, diff=" "):
    text = ""
    for i in s:
        text += diff + str(i)
    return text


# access_code finds  the access_code of from a response header
def access_code(s):
    access_code = ""
    for i in regex(s, "title"):
        if str(i).isdigit():
            access_code = str(i)
    return access_code


# tag finds text between any of two tags
def tag(st, start, end, included=True):
    new = st.split(start)[1:]
    new = string(new)
    new_2 = new.split(end)[0]
    return str(start) + str(new_2) + str(end)


# Getting the url from the arguments
input = ""
for i in sys.argv:
    if "http" in str(i):
        input = i

# Declaring and initiating host_name, port_name, path_name, file_name
host_name = ""
port_name = ""
path_name = ""
file_name = ""

# If the url doesn't starts with "http://", we return "ERR -arg 1"
if input[0:7] != 'http://':
    sys.exit("ERR -arg 1")
else:
    # Extracting host_name from the url
    host_name = input.split("/")[2]
    host_name = re.sub(":\w*", "", host_name)
    host_name = re.sub("\\\\\w*", "", host_name)

    # Extracting port_name from the url
    if len(input.split(":")) == 3:
        port_name = input.split("/")[2].split(":")[1]

    # Extracting path_name from the url
    if len(input.split("/")) >= 4:
        path_name = string(input.split("/")[3:], "/")

    # Default port_name
    if port_name == "":
        port_name = "80"

    # Default path_name
    if path_name == "":
        path_name = "/"

# print("Host:\t" + host_name)
# print("Port:\t" + port_name)
# print("Path:\t" + str(path_name))

# Trying to creating a scoket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

# Trying to get host ip form host name
try:
    remote_ip = socket.gethostbyname(host_name)
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

# Trying to connect with host (with ip and port)
try:
    s.connect((remote_ip, int(port_name)))
except:
    sys.exit("The host name or the port number is incorrect.\n")


def send():
    # GET Request
    if len(sys.argv) == 2:
        print('\n# Sending HTTP request to server')

        # Creating GET request
        request = "GET %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\n\r\n" \
                  % (path_name, host_name, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir")

        print(request)

        # Trying to send GET request
        try:
            s.sendall(request.encode('utf-8'))
        except socket.error:
            sys.exit('Send failed')

        print('# Receive data from server')

        # receive reponse from the server
        # reply --> header information
        # reply2 --> html code
        reply = s.recvfrom(4096)
        reply2 = s.recvfrom(4096)

        # Getting status_code and server_type
        status_code = int(str(reply).split("\n")[0].split(' ')[1])
        print("Response code: %s" % (status_code))
        server_type = string(re.findall("Server:(.*)", str(reply[0].decode('utf-8'))), "")
        print("Server Type: %s" % (server_type))

        # if status_code is 200-level, we extract last_modified and content_length,
        # save the htmol file in local directory and open it with default web browser
        if status_code >= 200 and status_code < 300:

            # Getting last_modified and content_length
            last_modified = string(re.findall("Last-Modified:(.*)", str(reply[0].decode('utf-8'))), "")
            content_length = string(re.findall("Content-Length:(.*)", str(reply[0].decode('utf-8'))), "")

            print("Last Modified Date: %s" % (last_modified))
            print("Number of bytes: %s" % (content_length))

            # Setting default path to index.html
            # otherwise, the path is the file name only
            if path_name == '/':
                file_name = "index.html"
            else:
                file_name = path_name.split('/')[-1]
            cwd = os.getcwd()

            # Create the html file and open it in the default web browser
            try:
                try:
                    open(format(cwd) + "/" + file_name, "w").write(html(reply2[0].decode('utf-8')))
                    print("Stored received file at %s" % (cwd + '\\' + file_name))
                    webbrowser.open('file://' + cwd + '\\' + file_name)
                except:
                    open(format(cwd) + "/" + file_name, "w").write(reply2[0].decode('utf-8').split("\n\r")[-1])
                    print("Stored received file at %s" % (cwd + '\\' + file_name))
                    webbrowser.open('file://' + cwd + '\\' + file_name)

            except:
                None

        # if status_code is 300-level, we extract permanently moved web address
        if status_code >= 300 and status_code < 400:
            moved = string(re.findall("Location:(.*)", str(reply[0].decode('utf-8'))), "")

            print("The File is located at: %s" % (moved))

        # Getting the header of the response of the server
        print("\n# HTTP Response Header")
        header = reply[0].decode('utf-8').split("\n\r")[0]

        print(header)


    # PUT Request
    elif len(sys.argv) == 4 and sys.argv[1].upper() == 'PUT':

        # Getting the file name from the arguments
        file_name = sys.argv[3]
        print('\n# Sending data to server')

        # Creating PUT request
        request = "PUT %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\nfiles: %s\r\n\r\n" \
                  % (file_name, host_name, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir", file_name)

        print(request)

        # Trying to send PUT request
        try:
            s.sendall(request.encode('utf-8'))
        except socket.error:
            print('Send failed\nThe host doesn\'t exist or the port given is not open')
            sys.exit()

        # Receive reponse from the server
        print('# Receive data from server')
        reply = s.recvfrom(4096)

        # Getting the status of the PUT request
        print(reply[0].decode().split("\n")[0])

        # Getting the status_code and server_type of the PUT request
        status_code = int(str(reply).split("\n")[0].split(' ')[1])
        print("Response code: %s" % (status_code))
        server_type = string(re.findall("Server:(.*)", str(reply[0].decode('utf-8'))), "")
        print("Server Type: %s" % (server_type))

    # If the PUT request doesn't have any valid file argument
    elif sys.argv[1].upper() == 'PUT':
        print("ERR -FILE NOT FOUND.")

    # If any of the request (PUT or GET) has more than required arguments return ERR - <extra argumetns>
    else:
        var = []
        for i in range(1, len(sys.argv)):
            var.append(i)
        print("ERR -%s" % (string(var, " ")))


# Trying to call the send function with commandline arguments unless there is a keyboard interruption
try:
    send()
except KeyboardInterrupt:
    pass
