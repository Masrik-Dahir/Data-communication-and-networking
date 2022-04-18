import sys

import requests
import socket
import datetime

fileName = "index.html"
openBin = {'file':(fileName,open(fileName,'rb').read())}
response = requests.put('http://httpstat.us/200',files=openBin)
print(response.headers)