import requests

response = requests.put('https://example.com/',
            data = {'key1':'value1', 'key2':'value2'})
print(response.headers)