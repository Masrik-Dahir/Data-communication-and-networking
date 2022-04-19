import socket
import datetime
import sys
import os
import re

arguments = sys.argv
# arguments = ['.\\HTTPClient.py', 'http://egr.vcu.edu']
# arguments = ['.\\HTTPClient.py', 'PUT', 'http://httpbin.org:80', "index.html"]


if len(arguments) <= 2:
    portCheck = True
    pathCheck = True
    url = arguments[1]
    if url[0:7] != 'http://':
        sys.exit("ERR -arg 1")
    #parse the url into hostname, port, and path
    try:
        url.split(":")[2]
        hostname = url.split(":")[1]
        hostname = hostname[2:len(hostname)]

    except:
        hostname = url.split("/")[2]
        portCheck = False

    if portCheck:
        try:
            url.split("/")[3]
            port = url.split("/")[2].split(":")[1]
        except:
            pathCheck = False
            port = url.split("/")[2].split(":")[1]
    else:
        port = '80'
    # print(port)
    if pathCheck:
        try:
            path = url.split("/")[3]
        except:
            path = "/"
    else:
        path = "/"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((hostname, int(port)))

    print('# Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    print('# Getting remote IP address')
    try:
        remote_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    print('# Connecting to server, ' + hostname + ' (' + remote_ip + ')')
    s.connect((remote_ip, int(port)))
    print('# Sending data to server')

    print(hostname)
    print(port)
    print(path)

    request = "GET %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\n\r\n" \
              % ("/", hostname, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir")

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


    # print(builtRequest.request.method + " " + builtRequest.request.url)
    # print("Host: " + builtRequest.request.headers['host'])
    # print("Time: " + builtRequest.request.headers['time'])
    #
    # print("Class-name: " + builtRequest.request.headers['class-name'])
    # print("User-name: " + builtRequest.request.headers['user-name'])
    # print()
    #
    # if status == 200:
    #     print("HTTP/1.1 200 OK")
    #     print("Date: " + builtRequest.headers['date'])
    #     try:
    #         print("Server: " + builtRequest.headers['server'])
    #     except:
    #         print("Server: Not Found")
    #     try:
    #         print("Last-Modified: " + builtRequest.headers['last-modified'])
    #     except:
    #         print("Last-Modified: Not Found")
    #     try:
    #         print("ETag: " + builtRequest.headers['etag'])
    #     except:
    #         print("ETag: Not Found")
    #     try:
    #         print("Accept-Ranges: " + builtRequest.headers['accept-ranges'])
    #     except:
    #         ("Accept-Ranges: Not Found")
    #     try:
    #         print("Content-Length: " + builtRequest.headers['content-length'])
    #     except:
    #         ("Content-Length: Not Found")
    #     try:
    #         print("Connection: " + builtRequest.headers['connection'])
    #     except:
    #         print("Connection: Not Found")
    #     try:
    #         print("Content-Type: " + builtRequest.headers['content-type'])
    #     except:
    #         print("Content-Type: Not Found")
    #
    # if (status >= 300) and (status < 400):
    #     if status == 301:
    #         print("HTTP/1.1 301 Moved Permanently")
    #     if status == 302:
    #         print("HTTP/1.1 302 Found")
    #     if status > 302:
    #         print("HTTP/1.1 " + str(status))
    #
    #     print("Date: " + builtRequest.headers['date'])
    #     try:
    #         print("Location: " + builtRequest.headers['location'])
    #     except:
    #         print("Location: Not Found")
    #     try:
    #         print("Server: " + builtRequest.headers['server'])
    #     except:
    #         print("Server: Not Found")
    #     try:
    #         print("Last-Modified: " + builtRequest.headers['last-modified'])
    #     except:
    #         print("Last-Modified: Not Found")
    #     try:
    #         print("ETag: " + builtRequest.headers['etag'])
    #     except:
    #         print("ETag: Not Found")
    #     try:
    #         print("Accept-Ranges: " + builtRequest.headers['accept-ranges'])
    #     except:
    #         ("Accept-Ranges: Not Found")
    #     try:
    #         print("Content-Length: " + builtRequest.headers['content-length'])
    #     except:
    #         ("Content-Length: Not Found")
    #     try:
    #         print("Connection: " + builtRequest.headers['connection'])
    #     except:
    #         print("Connection: Not Found")
    #     try:
    #         print("Content-Type: " + builtRequest.headers['content-type'])
    #     except:
    #         print("Content-Type: Not Found")
    #
    # cwd = os.getcwd()
    # open(format(cwd) + "/" + path, "wb").write(builtRequest.content)

elif arguments[1].upper() == 'PUT':
    url = arguments[2]
    pathCheck = True
    portCheck = True
    if url[0:7] != 'http://':
        sys.exit("ERR -arg 1")
    #parse the url into hostname, port, and path
    try:
        url.split(":")[2]
        hostname = url.split(":")[1]
        hostname = hostname[2:len(hostname)]
        print(hostname)
    except:
        hostname = url.split("/")[2]
        portCheck = False
        print(hostname)
    if portCheck:
        try:
            url.split("/")[3]
            port = url.split("/")[2].split(":")[1]
        except:
            pathCheck = False
            port = url.split("/")[2].split(":")[1]
    else:
        port = '80'
    print(port)
    if pathCheck:
        try:
            path = url.split("/")[3]
        except:
            path = "/"
    else:
        path = "/"
    print(path)


    print('# Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()


    print('# Getting remote IP address')
    try:
        remote_ip = socket.gethostbyname(hostname)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    print('# Connecting to server, ' + hostname + ' (' + remote_ip + ')')
    s.connect((remote_ip, int(port)))
    print('# Sending data to server')

    fileName = "index.html"
    openBin = {'file': (fileName, open(fileName, 'rb').read())}

    request = "PUT %s HTTP/1.0\r\nHost: %s\r\nTime: %s\r\nClass-name: %s\r\nUser-name: %s\r\nAccept: text/html\r\nfiles: %s\r\n" \
              % ("/", hostname, datetime.datetime.now(), "VCU-CMSC440-2022", "Masrik Dahir", openBin)

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



else:
    sys.exit("Invalid Args")