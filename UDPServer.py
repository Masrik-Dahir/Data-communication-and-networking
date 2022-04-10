# UDPServer.py

from socket import *
import sys

args = sys.argv
if len(args) != 2:
    print "Usage: python UDPServer.py port"
    exit()
port = int(args[1])

# Create welcoming socket using given port
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', port))

print 'Listening on port', port, '... '

# While loop to handle arbitrary sequence of clients making requests
while 1:
    # Waits for some client to send a packet
    clientSentence, clientAddress = serverSocket.recvfrom(2048)
    print 'FROM CLIENT:', clientSentence

    # Convert to all caps
    serverSentence = clientSentence.upper()

    # Write output line to socket
    serverSocket.sendto(serverSentence, clientAddress)
    print 'TO CLIENT:', serverSentence

