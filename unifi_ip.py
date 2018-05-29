import json
import os
import requests
import sys

base = 'https://unifi:8443'
session = requests.Session()
session.verify = False

login = {'username': os.environ.get('UNIFI_USERNAME'),
         'password': os.environ.get('UNIFI_PASSWORD')}
session.post(base + '/api/login', json=login)

device = {'macs': sys.argv[1:]}
response = session.post(base + '/api/s/default/stat/device', json=device)
content = response.json()

if 'ip' in content:
    print(content['ip'])
