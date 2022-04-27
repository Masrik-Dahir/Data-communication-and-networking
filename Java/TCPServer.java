import java.io.*;
import java.net.*;

class TCPServer {

    public static void main(String argv[]) throws Exception
    {
        // TCP socket variables
        ServerSocket welcomeSocket;
        Socket connectionSocket;

        // client variables
        String clientSentence, serverSentence;

        // command-line arguments
        int port;

        // process command-line arguments
        if (argv.length < 1) {
            System.out.println ("Usage: java TCPServer port\n");
            System.exit (-1);
        }
        port = Integer.parseInt(argv[0]);

        // Create welcoming socke t using the given port
        welcomeSocket = new ServerSocket(port);

        System.out.println("Listening on port " + port + "...");

        // While loop to handle arbitrary sequence of clients making requests
        while(true) {

            // Waits for some client to connect and creates new socket
            // for connection
            connectionSocket = welcomeSocket.accept();
            System.out.println("Client Made Connection");

            // Create (buffered) input stream attached to connection socket
            BufferedReader inFromClient = new BufferedReader(
                    new InputStreamReader(
                            connectionSocket.getInputStream()));

            // Create output stream attached to connection socket
            DataOutputStream outToClient = new DataOutputStream(
                    connectionSocket.getOutputStream());

            // Read input line from socket
            clientSentence = inFromClient.readLine();
            System.out.println("FROM CLIENT: " + clientSentence);

            // Capitalize the sentence
            serverSentence = clientSentence.toUpperCase();

            // Write output line to socket (add a newline)
            outToClient.writeBytes(serverSentence + '\n');
            System.out.println ("TO CLIENT: " + serverSentence);

            // Close the connection socket
            connectionSocket.close();

        } //  end while; loop back to accept a new client connection

    } // end main

} // end class
