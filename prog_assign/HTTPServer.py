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
    arg = string(re.findall("(?<=%s:).*" % (var), st))
    arg = re.sub("^\s+", "", arg)
    return arg


def main():
    try:

        # Ceckinig if the are two arguments (the python file and port) and the port number is possitive and less than 65536
        if len(sys.argv) == 2 and int(sys.argv[1]) > 0 and int(sys.argv[1]) < 65536:

            # Creating socket listening for GET or PUT request
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_port = int(sys.argv[1])
            server.bind(('', server_port))
            server.listen(1)
        else:

            # If the condiotn does't meet or the port is busy, we return "ERR -arg -1"
            ag = ""
            for i in range(1, len(sys.argv)):
                ag += str(i) + " "
            sys.exit("ERR -arg %s" % (ag))

    # If there are more than or less than two command line arguments, we return the ERR -arg <arguments numbers>
    except:
        ag = ""
        for i in range(1, len(sys.argv)):
            ag += str(i) + " "
        sys.exit("ERR -arg %s" % (ag))

    print("The server is ready to receive at PORT: %s" % (server_port))

    # ALways true while loop to wait for GET or PUT request unless there is a Ctrl-C keyboard interruption
    while 1:

        # Getting connection_socket and addr of the client
        connection_socket, addr = server.accept()

        # reading the HTTP request
        sentence = connection_socket.recv(1024).decode()

        # Parsing the request type
        request_type = str(sentence.split("\n\r")[0].split(" ")[0])

        # Printing out the Client ip:port:request
        print("\n# Client IP address, port, and request")
        print(str(addr[0]) + ":" + str(addr[1]) + ":" + request_type)

        # Printing out HTTP request
        print("\n# Client HTTP request")
        print(sentence)

        # PUT Request
        if request_type.upper() == "PUT":

            # formattig filename properly, so we can use it later to create the html file
            try:
                filename = str(sentence.split()[1])
                lines = ""
                if filename.startswith("/"):
                    filename = str(filename)[1:]
                elif filename.startswith("./"):
                    filename = str(filename)[2:]
                elif filename.startswith("\\"):
                    filename = str(filename)[1:]

                # Reading the file content of the request PUT file
                with open(filename) as f:
                    lines = f.read()
                directory = './'
                first = filename.split("/")[-1]
                second = first.split("\\")[-1]

                # Crerating the file in the local directory
                file_path = os.path.join(directory, second)

                # Writing the file with the content of the PUT file
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                file = open(file_path, "w")
                file.write(lines)
                file.close()

                # Responding with "OK File Created" to the client
                response = 'HTTP/1.0 200 OK File Created\r\nServer: %s\r\n\r\n' % (str(os.getenv('HOSTNAME')))

            # Otherwise if file not created, responding with "606 File NOT Created" to client
            except:
                response = 'HTTP/1.0 606 File NOT Created\r\n\r\n'

            # sending  the resond message
            connection_socket.send(response.encode('utf-8'))
            connection_socket.close()

        # GET Request
        if request_type.upper() == "GET":

            # Formatting file name
            filename = "." + sentence.split()[1]

            # Setting default file name to index.html
            if filename == './':
                filename = './index.html'

            # Reading the file content and saving it to lines
            if exists(filename):
                with open(filename, 'rb') as file:
                    lines = file.read()

                # Creating response message
                response = 'HTTP/1.0 200 OK\r\nConnection: close\r\nServer: %s\r\nLast-Modified: %s\r\nContent-Length: %s\r\n\r\n'.encode(
                    'utf-8') % (str(os.getenv('HOSTNAME')).encode('utf-8'),
                                datetime.now().strftime("%a, %d %b %Y %H:%M:%S").encode('utf-8'),
                                str(len(lines)).encode('utf-8'))

                # Seinding the response header message
                connection_socket.send(response)

                # Sending the file contents
                connection_socket.send(lines)

                # Closing the socket
                connection_socket.close()

            # Otherwise if the file doens not exist, we return "404 Not Found"
            else:
                response = 'HTTP/1.0 404 Not Found\n'.encode('utf-8')
                connection_socket.send(response)
                connection_socket.close()


if __name__ == '__main__':

    # Trying to call the main function
    try:
        main()

    # If there is a Keyboard Interruption, we break exist the system with message Keyboard Interruption (Ctrl-C)
    except KeyboardInterrupt:
        print('\nKeyboard Interruption (Ctrl-C)')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)