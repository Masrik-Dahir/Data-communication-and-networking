# """
#  Implements a simple HTTP/1.0 Server
#
# """
#
# import socket as http_server_socket
#
#
# # Define socket host and port
# server_ip = '127.0.0.1'
# server_port = 8000
#
# # Create socket
# socket_1 = http_server_socket.socket(http_server_socket.AF_INET, http_server_socket.SOCK_STREAM)
# socket_1.setsockopt(http_server_socket.SOL_SOCKET, http_server_socket.SO_REUSEADDR, 1)
# socket_1.bind((server_ip, server_port))
# socket_1.listen(1)
# print('Listening on port %s ...' % server_port)
#
# while True:
#     # Wait for client connections
#     client_connection, client_address = socket_1.accept()
#
#     # Get the client request
#     request = client_connection.recv(1024).decode()
#     print(request)
#
#     # Parse HTTP headers
#     headers = request.split('\n')
#     filename = str(headers[0].split()[1]).replace('/','')
#     if filename == "":
#         filename = "index.html"
#
#     # Get the content of htdocs/index.html
#     try:
#         fin = open(str(filename))
#         content = fin.read()
#         fin.close()
#         response = 'HTTP/1.0 200 OK\n\n' + content
#
#     except FileNotFoundError:
#         response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'
#
#     # Send HTTP response
#     client_connection.sendall(response.encode())
#     client_connection.close()
#
# #
#
# # Close socket
# socket_1.close()







import os
import socket
server_port = 12000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', server_port))
server.listen(1)

print ("The server is ready to receive")
while 1:
    print ("Waiting ...")
    connection_socket, addr = server.accept()
    print ("accept")
    sentence = connection_socket.recv(2048).decode()
    print ("Message Received: \n" + sentence)





    # Get the content of htdocs/index.html
    try:
        filename = sentence.split()[1]
        lines = ""
        with open(filename) as f:
            lines = f.read()
        print(lines)
        directory = './HTTPServer_html/'
        file_path = os.path.join(directory, filename)
        if not os.path.isdir(directory):
            os.mkdir(directory)
        file = open(file_path, "w")
        file.write(lines)
        file.close()
        response = 'HTTP/1.0 200 OK\r\nFile: %s\r\n\r\n' % (filename)

    except FileNotFoundError:
        response = 'HTTP/1.0 404 NOT FOUND\n\nFile Not Found'





    modifiedSentence = 'Message Received!'

    connection_socket.send(response.encode('utf-8'))
    connection_socket.close()