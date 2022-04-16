import requests
import datetime
import sys
import re


input = str(sys.argv[1])
addSlash = False
p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*)(?P<path>[^\s]*)'
link = re.search(p,input)

host_name = link.group('host')

port_name = link.group('port')
if port_name == "":
    port_name = "80"
    addSlash = True

path_name = link.group('path')
if addSlash:
    path_name = "/"+path_name
if path_name == "":
    path_name = "/"


x = requests.get(input, params={'Host': host_name, 'Time': str(datetime.datetime.now()), 'Class-name': 'VCU-CMSC440-2022', 'User-name': 'Masrik Dahir'})
print(x.headers)

