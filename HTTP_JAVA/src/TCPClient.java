import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.URLEncoder;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TCPClient {

    private static int access_code(String text){
        int access_code = 400;
        Pattern pattern = Pattern.compile("<title>(.+?)</title>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(text);
        matcher.find();
        Pattern p = Pattern.compile("\\d+");
        Matcher m = p.matcher(matcher.group(1).toString());
        while(m.find()) {
            access_code = Integer.parseInt(m.group());
        }

        return access_code;
    }
    private static String last_modified(String text){
        Matcher m = Pattern.compile("Last-Modified:(.*)").matcher(text);
        String result = "";
        if (m.find())
        {
            result += (m.group(1)).toString();
        }
        return result.replace(" ", "");
    }

    private static String server(String text){
        Matcher m = Pattern.compile("Server:(.*)").matcher(text);
        String result = "";
        if (m.find())
        {
            result += (m.group(1)).toString();
        }
        return result.replace(" ", "");
    }

    private static String content_length(String text){
        Matcher m = Pattern.compile("Content-Length:(.*)").matcher(text);
        String result = "";
        if (m.find())
        {
            result += (m.group(1)).toString();
        }
        return result.replace(" ", "");
    }

    private static String link(String text){
        Pattern pattern = Pattern.compile("<a[\\s\\S]*?href=\"([^\"]+)\"[\\s\\S]*?>", Pattern.DOTALL);
        Matcher matcher = pattern.matcher(text);
        matcher.find();

        return matcher.group(1).toString();
    }

    public static void main(String[] args) {

        try {

            String params = URLEncoder.encode("param1", "UTF-8")
                    + "=" + URLEncoder.encode("value1", "UTF-8");
            params += "&" + URLEncoder.encode("param2", "UTF-8")
                    + "=" + URLEncoder.encode("value2", "UTF-8");

            String hostname = "egr.vcu.edu";
            int port = 80;
            String path = "/";

            String removed_http = args[0].split("//")[1];
            int counter = 0;

            for (String i: removed_http.split("/")){

                if (counter == 0){
                    hostname = i;
                }
                if (counter > 0){
                    path += i + "/";
                }
                counter ++;
            }

            if (hostname.contains(":")){
                port = Integer.parseInt(hostname.split(":")[1]);
                hostname = hostname.split(":")[0];
            }

            if (path.equals("/")){
                path = "/index.html";
            }

            else if (path.endsWith("/")){
                path = path.substring(0, path.length()-1);
            }


            System.out.println("Host: " + hostname);
            System.out.println("Port: " + port);
            System.out.println("Path: " + path);


            try{
                InetAddress addr = InetAddress.getByName(hostname);
                Socket socket = new Socket(addr, port);

                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("EEE, dd MMM yyyy HH:mm:ss O");
                String date = formatter.format(ZonedDateTime.now(ZoneOffset.UTC));


                // Send headers
                BufferedWriter wr =
                        new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF8"));
                String request = "";
                wr.write("GET "+path+" HTTP/1.0\r\n");
                request += "GET "+path+" HTTP/1.0\r\n";
                wr.write("Host: "+hostname+"\r\n");
                request += "Host: "+hostname+"\r\n";
                wr.write("Time: "+ date +"\r\n");
                request += "Time: "+ date +"\r\n";
                wr.write("Class-name: VCU-CMSC440-2022 \r\n");
                request += "Class-name: VCU-CMSC440-2022 \r\n";
                wr.write("User-name: Freja Halter \r\n");
                request += "User-name: Freja Halter \r\n";
                wr.write("Content-Length: "+params.length()+"\r\n");
                request += "Content-Length: "+params.length()+"\r\n";
                wr.write("Content-Type: application/x-www-form-urlencoded\r\n");
                request += "Content-Type: application/x-www-form-urlencoded\r\n";
                wr.write("\r\n");
                request += "\r\n";

                System.out.println("\nRequest to Server\n" + request);


                // Send parameters
                wr.write(params);
                wr.flush();

                // Get response
                BufferedReader rd = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                String line;
                String result = "";
                while ((line = rd.readLine()) != null) {
                    result += line + "\n\r";
                }
                String val[] = result.split("\n\r\n\r");
            /*
            val[0] header file
            val[1] heml file
             */

            /*
            Getting Access code
             */

                int access_code = access_code(val[1]);
                System.out.println("\nResponse from Server");
                System.out.println("Access code: " + access_code);
                System.out.println("Server: " + server(val[1]));
//            System.out.println(val[0]);
                if (access_code >= 200 && access_code < 300){
                    System.out.println("Last Modified: " + last_modified(val[0]));
                    System.out.println("Content Length: " + content_length(val[0]));

                }
                else if (access_code >= 300 && access_code < 400){
                    System.out.println("The File is moved to " + link(val[1]));

                }

                wr.close();
                rd.close();

            }
            catch (Exception e){
                System.out.println("Invalid url or port number");
            }

        }
        catch (Exception e) {
            e.printStackTrace();
        }

    }

}