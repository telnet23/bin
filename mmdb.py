import argparse
import maxminddb
import json
import os
import re
import sys

parser = argparse.ArgumentParser(allow_abbrev=False, description='Query MaxMind GeoIP2 and GeoLite2 databases.')
parser.add_argument('-d', '--directory', action='append', help='database directory')
parser.add_argument('ip', action='store', help='ip address')
args = parser.parse_args()

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
                typ = match.group(1)
                path = os.path.join(root, filename)
                reader = maxminddb.open_database(path)
                readers.append(reader)

readers = []
if not args.directory:
    args.directory = ['.']
for directory in args.directory:
    load_from(directory)
for reader in readers:
    try:
        record = reader.get(args.ip)
    except Exception as exception:
        print(exception, file=sys.stderr)
        continue
    if record:
        record['metadata'] = vars(reader.metadata())
        json.dump(record, fp=sys.stdout, sort_keys=True)
