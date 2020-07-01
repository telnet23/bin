import argparse
import json
import geoip2.database
import os
import pytz
import re
import requests
import socket

from collections import defaultdict
from datetime import datetime

def load_from(base):
    for root, directories, filenames in os.walk(base):
        for directory in directories:
            match = re.match('^Geo(?:IP|Lite)2-(?:.+)_(?:.+)$', directory)
            if match:
                path = os.path.join(root, directory)
                load_from(path)
        for filename in filenames:
            match = re.match('^Geo(?:IP|Lite)2-(.+)\.mmdb$', filename)
            if match:
                method = match.group(1).lower().replace('-', '_')
                path = os.path.join(root, filename)
                reader = geoip2.database.Reader(path)
                readers[method].append(reader)

def get(ip, method):
    i = 0
    record = None
    newest = None
    while i < len(readers[method]):
        try:
            record = getattr(readers[method][i], method)(ip)
        except:
            record = None
        i += 1
        if record is None:
            continue
        if newest is None:
            newest = record
        if method == 'city':
            if record.city.name is None:
                continue
        break
    return record

def geoip(ip):
    connection_type = get(ip, 'connection_type')
    asn = get(ip, 'asn')
    isp = get(ip, 'isp')
    city = get(ip, 'city')

    rows = []
    rows.append(['\x1B[37m', 'IP Address', ip])

    try:
        ghba = socket.gethostbyaddr(ip)
    except (socket.gaierror, socket.herror):
        pass
    else:
        # IP address may have multiple PTR records
        rows.append(['\x1B[37m', 'Hostname', ghba[0]])
        for additional in ghba[1]:
            if additional.endswith('.arpa'):
                continue
            rows.append(['\x1B[37m', 'Hostname', additional])

    if connection_type:
        if connection_type.connection_type:
            rows.append(['\x1B[33m', 'Connection Type', connection_type.connection_type])
    if asn:
        if asn.autonomous_system_number:
            rows.append(['\x1B[33m', 'Autonomous System', 'AS{} {}'.format(
                asn.autonomous_system_number, asn.autonomous_system_organization)])
    if isp:
        if isp.isp:
            rows.append(['\x1B[33m', 'Service Provider', isp.isp])
        if isp.organization and isp.organization != isp.isp:
            rows.append(['\x1B[33m', 'Organization', isp.organization])

    if city:
        if city.registered_country.name:
            rows.append(['\x1B[32m', 'Registered Country', city.registered_country.name])

        if city.continent.name:
            rows.append(['\x1B[32m', 'Continent', city.continent.name])

        if city.country.name:
            rows.append(['\x1B[32m', 'Country', city.country.name])

        for subdivision in city.subdivisions:
            if subdivision.name:
                rows.append(['\x1B[36m', 'Subdivision', subdivision.name])

        if city.city.name:
            rows.append(['\x1B[36m', 'City', city.city.name])

        if city.postal.code:
            rows.append(['\x1B[36m', 'Postal Code', city.postal.code])

        if city.location.time_zone:
            tz = city.location.time_zone
            offset = datetime.now(pytz.timezone(tz)).strftime('%z')
            rows.append(['\x1B[34m', 'Time Zone', f'{tz} (UTC{offset})'])

        if city.location.latitude and city.location.longitude:
            s = '{}, {}'.format(city.location.latitude, city.location.longitude)
            if city.location.accuracy_radius:
                s += ' (+/- {} km)'.format(city.location.accuracy_radius)
            rows.append(['\x1B[34m', 'Latitude, Longitude', s])

    maxlen = max(len(row[1]) for row in rows)
    for row in rows:
        print(f'{row[0]}{row[1]: <{maxlen}}  \x1B[1m{row[2]}\x1B[21m\x1B[39m')

def my_ip():
    try:
        return requests.get('https://api.ipify.org').text
    except requests.exceptions.ConnectionError:
        return None
 
parser = argparse.ArgumentParser(allow_abbrev=False, description='Query MaxMind GeoIP2 and GeoLite2 databases.')
parser.add_argument('-d', '--directory', action='append', help='database directory')
parser.add_argument('ip', nargs='*', help='ip address')
args = parser.parse_args()

readers = defaultdict(list)
if not args.directory:
    args.directory = ['.']
for directory in args.directory:
    load_from(directory)
for method in readers:
    readers[method].sort(key=lambda reader: reader.metadata().build_epoch, reverse=True)

ips = []
if args.ip is None:
    ips.append(my_ip())
else:
    for arg in args.ip:
        if arg == '?':
            ip = my_ip()
            if ip not in ips:
                ips.append(ip)
            continue

        try:
            # Try as IP address
            # IP address is canoncicalized
            ip = socket.inet_ntoa(socket.inet_aton(arg))
        except OSError:
            pass
        else:
            if ip not in ips:
                ips.append(ip)
            continue
    
        try:
            # Try as hostname
            # An arbitrary port number is required
            gai = socket.getaddrinfo(arg, 1)
        except (socket.gaierror, socket.herror):
            pass
        else:
            for info in gai:
                ip = info[-1][0]
                if ip not in ips:
                    ips.append(ip)
            continue

for i in range(len(ips)):
    geoip(ips[i])
    if i+1 < len(ips):
        print()
