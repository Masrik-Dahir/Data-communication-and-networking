Masrik Dahir V00894127

To run HTTPServer.py
    python HTTPServer.py <port>

To run HTTPClient.py
    python HTTPClient.py http://<ip_address>:<port>
    python HTTPClient.py http://<url>/<file_name>

Example of executing HTTPServer.py:
    (1) python HTTPServer.py 10004

Example of executing HTTPClient.py:
    GET Request
    (1) python HTTPClient.py http://172.18.233.74:10004/HTML/index.html
    (2) python HTTPClient.py http://172.18.233.74:10004
    (3) python HTTPClient.py http://egr.vcu.edu
    (4) python HTTPClient.py http://www.testingmcafeesites.com/

    PUT Request
    (1) python PUT HTTPClient.py http://172.18.233.74:10004 HTML/index.html

