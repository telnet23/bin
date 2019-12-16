#!/usr/bin/env python3

import json
import os
import requests
import socket
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('ddns.dat') as dat:
    previous_ip = dat.read()
    print('Previous IP address is', previous_ip)

current_ip = requests.get('https://api.ipify.org').text
print('Current IP address is', current_ip)

try:
    current_ip = socket.inet_ntoa(socket.inet_aton(current_ip))
except OSError:
    print('Error: Current IP address is not valid')
    sys.exit(1)

if previous_ip == current_ip:
    sys.exit()

domain = os.environ.get('DDNS_DOMAIN')
secret = os.environ.get('DDNS_SECRET')
key = os.environ.get('DDNS_KEY')

cpanel_ip = socket.gethostbyname('cpanel' + '.' + domain)
print('cpanel' + '.' + domain, 'IP address is', cpanel_ip)

for subdomain in {'@', 'vpn', 'www'}:
    if subdomain == '@':
        fqdn = domain
    else:
        fqdn = subdomain + '.' + domain

    subdomain_ip = socket.gethostbyname(fqdn)
    print(fqdn, 'IP address is', subdomain_ip)

    if subdomain_ip == current_ip:
        continue
    if subdomain_ip == cpanel_ip and subdomain != 'vpn':
        continue

    url = 'https://api.godaddy.com/v1/domains/{}/records/A/{}'.format(domain, subdomain)
    headers = {'Authorization': 'sso-key {}:{}'.format(key, secret), 'Content-Type': 'application/json'}
    data = json.dumps([{'data': current_ip}])
    response = requests.put(url, headers=headers, data=data)

    if response.status_code != 200:
        print('Error: Status code is', response.status_code)

with open('ddns.dat', 'w') as dat:
    dat.write(current_ip)
