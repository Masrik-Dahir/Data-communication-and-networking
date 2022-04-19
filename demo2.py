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

    print(filename)









    modifiedSentence = 'Message Received!'


    connection_socket.send(modifiedSentence.encode('utf-8'))
    connection_socket.close()