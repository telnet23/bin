#!/usr/bin/env python3

import requests
import sys
import os

zid = os.environ.get('DDNS_ZID')
rid = os.environ.get('DDNS_RID')
key = os.environ.get('DDNS_KEY')

url = f'https://api.cloudflare.com/client/v4/zones/{zid}/dns_records/{rid}'
headers = {'Authorization': f'Bearer {key}'}

response = requests.get(url, headers=headers).json()
print(response, file=sys.stderr)
existing = response['result']['content']
print('Record IP address is', existing)

response = requests.get('https://api.ipify.org?format=json').json()
print(response, file=sys.stderr)
actual = response['ip']
print('Actual IP address is', actual)

if existing != actual:
    response = requests.patch(url, headers=headers, json={'content': actual}).json()
    print(response, file=sys.stderr)
    print('Record IP address set to actual IP address')
