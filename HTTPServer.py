from datetime import datetime
import os
import sys
import re
import socket
from os.path import exists

def string(s, diff=" "):
    text = ""
    for i in s:
        text += diff + str(i)
    return text

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


    print ("The server is ready to receive at port: %s" %(server_port))

    while 1:
        print ("Waiting ...")
        connection_socket, addr = server.accept()
        print ("accept\n")
        sentence = connection_socket.recv(2048).decode()
        request_type = str(sentence.split("\n\r")[0].split(" ")[0])

        # Printing client's ip + port + request type
        print(str(addr[0]) + ":" + str(addr[1]) + ":" + request_type)

        # Printing ech line in HTTP body
        print(sentence)


        # Get the content of htdocs/index.html

        if request_type.upper() == "PUT":
            try:
                filename = sentence.split()[1]
                lines = ""
                with open(filename) as f:
                    lines = f.read()
                print(lines)
                directory = './'
                first = filename.split("/")[-1]
                second = first.split("\\")[-1]
                file_path = os.path.join(directory, second)

                if not os.path.isdir(directory):
                    os.mkdir(directory)
                print(file_path)
                file = open(file_path, "w")
                file.write(lines)
                file.close()

                # Printing valid HTTP response
                response = 'HTTP/1.0 200 OK File Created\r\n'

            except FileNotFoundError:
                response = 'HTTP/1.0 606 File NOT Created\r\n'


            modifiedSentence = 'Message Received!'
            connection_socket.send(response.encode('utf-8'))
            connection_socket.close()

        if request_type.upper() == "GET":

            filename = "." + sentence.split()[1]

            if filename == './':
                filename = './index.html'

            # print(filename)
            if exists(filename):
                with open(filename, 'rb') as file:
                    lines = file.read()
                # print(lines.decode('utf-8'))

                # Printing valid HTTP response
                response = 'HTTP/1.0 200 OK\nServer: %s\nLast-Modified: %s\nContent-Length: %s\n\n%s\n'.encode('utf-8') %(str(os.getenv('HOSTNAME')).encode('utf-8'), datetime.now().strftime("%a, %d %b %Y %H:%M:%S").encode('utf-8'), str(len(lines)).encode('utf-8'), lines)

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