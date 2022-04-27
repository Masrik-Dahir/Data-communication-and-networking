import java.io.*;
import java.net.*;
import java.text.SimpleDateFormat;
import java.util.Date;

class TCPClient {

    // command-line arguments
    static int isPort = 1;
    static String getOrPut;
    static String hostName = "www.testingmcafeesites.com";
    static String path = "/index.html";
    static String fileName = "";
    static String port = "80";

    public static void main(String argv[]) throws Exception
    {
        // TCP socket variables
        Socket clientSocket;
        DataOutputStream outToServer;
        BufferedReader inFromServer;

        // client variables
        BufferedReader inFromUser;
        String clientSentence, serverSentence;

        // command-line arguments
//        String server;
//        int port;

        // process command-line arguments
//        if (argv.length < 2) {
//            System.out.println ("Usage: java TCPClient hostname port\n");
//            System.exit (-1);
//        }
//        server = argv[0];
//        port = Integer.parseInt(argv[1]);

        //the argument taken from the command line before anything is done to it
        String originalArg = argv[0];

        //lets us know if a port is involved or not
        String delimIsPort = "[:]";
        String[] portTest = originalArg.split(delimIsPort);
        if (portTest.length <= 1) {
            port = "80"; //no port value was given from command line
            isPort = 0;
            if (portTest.length < 1) {
                System.out.println("ERR - arg 0"); // http:// was never given at the start if there is only 1 arg in array
            }
        }

        //splits the argument, assuming a port is there
        String delimPort = ":|/";
        String[] withPort = originalArg.split(delimPort);

        try{
            if(withPort[0] == "http" && withPort[1] == "" && withPort[2] == ""){
                int x = 0;
            }
        }
        catch(ArrayIndexOutOfBoundsException E){
            System.out.println("ERR - arg 1"); // the website given did not begin with http://
        }

        for(int i = 0; i < withPort.length; i++)
        //gets the details if a port was added
        if (isPort == 1) {
            hostName = withPort[3];
            port = withPort[4];

            //since the delim seperated each part of the path, we combine it together here
            if(withPort.length > 5) {
                int x;
                for (x = 5; x <= withPort.length; x++) {
                    path = path + "/" + withPort[x];
                }
            }
            else{
                path = "/";
            }
        }
        //if a port wasn't added
        else {
            hostName = withPort[3];

            //same reason for loop as above
            if(withPort.length > 4) {
                int y;
                for (y = 4; y <= withPort.length; y++) {
                    path = path + "/" + withPort[y];
                }
            }
            else{
                path ="/";
            }
        }

        // Create (buffered) input stream using standard input
//        inFromUser = new BufferedReader(new InputStreamReader(System.in));

        // Create client socket with connection to server at given port
        clientSocket = new Socket (hostName, Integer.parseInt(port));

        // Create output stream attached to socket
        outToServer = new DataOutputStream(clientSocket.getOutputStream());

        // Create (buffered) input stream attached to socket
        inFromServer = new BufferedReader(new InputStreamReader(
                clientSocket.getInputStream()));

        // Read line from user
//        System.out.println("Client ready for input");
//        clientSentence = inFromUser.readLine();

        //for getting the current time
        SimpleDateFormat date = new SimpleDateFormat("EEE dd MMM yyyy HH:mm:ss z");
        Date now = new Date(System.currentTimeMillis());
//        clientSentence = "GET " + path + " HTTP/1.0\r\nHOST: " + hostName + "\r\nDATE: " + date.format(now) + "\r\nClass-name: VCU-CMSC440-2022\r\nUser-name: Freyja Halter\r\n\r\n";
        clientSentence = "GET "+ path /*filename*/ + " HTTP/1.0\r\n"
            + "Host: " +hostName+ " \r\n"/*hostName*/
            + "Date: " + date.format(now) + "\r\n"
            + "Class Name: VCU-CMSC440-2020\r\n"
            + "User Name: Freyja Halter\r\n"
            + "Accept-Encoding: gzip\r\n"
            + "Connection: close\r\n\r\n";

        //try to send line to server
        try {
            outToServer.writeBytes(clientSentence + "\r\n");
        } catch (Exception e) {
            System.out.println("Send Failed");
        }

        String hReply = "";
        String htReply = "";
        String x = "";

        //LOOK AT THIS LATER"
        //replies from the server
        System.out.println(1);
        while (inFromServer.readLine() != "\r\n" && inFromServer.readLine() != null)
            hReply = hReply + inFromServer.readLine();
        System.out.println(2);
        while (inFromServer.readLine() == "\r\n")
            x = inFromServer.readLine(); //just skips the empty lines
        System.out.println(3);
        while (inFromServer.readLine() != "\r\n" && inFromServer.readLine() != null)
            htReply = htReply + inFromServer.readLine();

        //extrapolates certain data from the server response
        int statusCode;
        String serverType;
        String[] statCode;
        String[] typeCode, typeCode2;

        //gets the status code
        statCode = (hReply.split(" "));
        statusCode = Integer.parseInt(statCode[1]);

        //gets the Server type code
        typeCode = (hReply.split("Server:"));
        typeCode2 = typeCode[1].split("\n");
        serverType = typeCode2[0];

        //statusCode = Integer.parseInt((headerReply).toString().split("\n", 0).split(' ', 1));
        System.out.println("Response code: " + statusCode + "\r\n");
        System.out.println("Server type: " + serverType + "\r\n");

        //does different things depending on the status code recieved
        if (statusCode >= 200 && statusCode < 300) {
            String[] modifySplit, modifySplit2;
            String Modify;

            String[] contentSplit, contentSplit2;
            String contentLength;

            //gets the last modified date
            modifySplit = (hReply.split("Last-Modified:"));
            modifySplit2 = modifySplit[1].split("\n");
            Modify = modifySplit2[0];

            //gets the length of the content
            contentSplit = (hReply.split("Content-Length:"));
            contentSplit2 = contentSplit[1].split("\n");
            contentLength = contentSplit2[0];

            //displays the last modified date and how many bytes the message is
            System.out.println("Last Modified Date: " + Modify + "\r\n");
            System.out.println("Number of Bytes: " + contentLength + "\r\n");

            //sets default path to
            if (path == "/") {
                fileName = "index.html";
            } else {
                String[] fileArray;
                fileArray = path.split("/", -1);
                for(int i = 0; i <fileArray.length; i++){
                    fileName = fileName + fileArray[i];
                }
            }

            //create the HTML file and open it in the default web browser
            try {
                File myObj = new File(fileName);
                if (myObj.createNewFile()) {
                    System.out.println("File created: " + myObj.getName());
                } else {
                    System.out.println("File already exists.");
                }
            } catch (IOException e) {
                System.out.println("An error occurred.");
                e.printStackTrace();
            }

            FileInputStream is = null;
            FileOutputStream os = null;

            try {
                is = new FileInputStream(fileName);
                os = new FileOutputStream(fileName);
                byte[] buffer = new byte[1024];
                int length;
                while ((length = is.read(buffer)) > 0) {
                    os.write(buffer, 0, length);
                }
            } finally {
                is.close();
                os.close();
            }

        } else {
            if (statusCode >= 300 && statusCode < 400) {
                String[] move, move2;
                String loc;

                //gets the last known location
                move = (hReply.split("Location:"));
                move2 = move[1].split("\n");
                loc = move[0];

                System.out.println("The file is located at: " + loc + "\r\n");
            }
        }

        // Write line to server (add newline)
        /*outToServer.writeBytes(clientSentence + '\n');
        System.out.println ("TO SERVER: \n" + clientSentence);

        // Read line from server
        serverSentence = inFromServer.readLine();
        System.out.println("FROM SERVER: " + serverSentence);
        */
        // Close the socket
        clientSocket.close();

    } // end main

} // end class
