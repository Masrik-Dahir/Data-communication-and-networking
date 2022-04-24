# ----------------------------------------------------
#  Masrik Dahir
#  Date: 04/24/2022
#
#  ---------------------------------------------------
#  Usage Guide
#  (1) python HTTPServer.py 10004
#
# ----------------------------------------------------

from datetime import datetime
import os
import sys
import re
import socket
from os.path import exists

# string converts a list to string with a preffered seperator
# string(["a", "b", "c"], " ") --> "a b c"
def string(s, diff=" "):
    text = ""
    for i in s:
        text += diff + str(i)
    return text

# semicolon function finds the phrases after semicolon of a an attribute i.e. "Host: egr.vcu.edu" --> "egr.vcu.edu"
def semicolon(st, var):
    arg = string(re.findall("(?<=%s:).*" %(var), st))
    arg = re.sub("^\s+","", arg)
    return arg

def main():
    try:
        if len(sys.argv) == 2 and int(sys.argv[1])>0 and int(sys.argv[1]) < 65536:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_port = int(sys.argv[1])
                server.bind(('', server_port))
                server.listen(1)
        else:
            ag = ""
            for i in range(1,len(sys.argv)):
                ag += str(i) + " "
            sys.exit("ERR -arg %s" %(ag))
    except:
            ag = ""
            for i in range(1, len(sys.argv)):
                ag += str(i) + " "
            sys.exit("ERR -arg %s" % (ag))


    print ("The server is ready to receive at PORT: %s" %(server_port))

    while 1:
        connection_socket, addr = server.accept()
        sentence = connection_socket.recv(1024).decode()
        request_type = str(sentence.split("\n\r")[0].split(" ")[0])

        print("\n# Client IP address, port, and request")
        print(str(addr[0]) + ":" + str(addr[1]) + ":" + request_type)

        print("\n# Client HTTP request")
        print(sentence)


        if request_type.upper() == "PUT":
            try:
                filename = str(sentence.split()[1])
                lines = ""
                if filename.startswith("/"):
                    filename = str(filename)[1:]
                elif filename.startswith("./"):
                    filename = str(filename)[2:]
                elif filename.startswith("\\"):
                    filename = str(filename)[1:]


                with open(filename) as f:
                    lines = f.read()
                directory = './'
                first = filename.split("/")[-1]
                second = first.split("\\")[-1]
                file_path = os.path.join(directory, second)

                if not os.path.isdir(directory):
                    os.mkdir(directory)
                file = open(file_path, "w")
                file.write(lines)
                file.close()

                response = 'HTTP/1.0 200 OK File Created\r\nServer: %s\r\n\r\n' %(str(os.getenv('HOSTNAME')))

            except:
                response = 'HTTP/1.0 606 File NOT Created\r\n\r\n'


            connection_socket.send(response.encode('utf-8'))
            connection_socket.close()

        if request_type.upper() == "GET":

            filename = "." + sentence.split()[1]

            if filename == './':
                filename = './index.html'

            if exists(filename):
                with open(filename, 'rb') as file:
                    lines = file.read()

                response = 'HTTP/1.0 200 OK\r\nConnection: close\r\nServer: %s\r\nLast-Modified: %s\r\nContent-Length: %s\r\n\r\n'.encode('utf-8') %(str(os.getenv('HOSTNAME')).encode('utf-8'), datetime.now().strftime("%a, %d %b %Y %H:%M:%S").encode('utf-8'), str(len(lines)).encode('utf-8'))
                connection_socket.send(response)
                connection_socket.send(lines)
                connection_socket.close()



            else:
                response = 'HTTP/1.0 404 Not Found\n'.encode('utf-8')
                connection_socket.send(response)
                connection_socket.close()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nKeyboard Interruption (Ctrl-C)')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)