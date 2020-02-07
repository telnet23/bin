#!/usr/bin/env python3

import argparse
import json
import os
import re
import requests
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory')
parser.add_argument('-p', '--prefix')
parser.add_argument('-u', '--user-agent')
parser.add_argument('url', nargs='+')
args = parser.parse_args()

session = requests.Session()
if args.user_agent is not None:
    session.headers.update({'User-Agent': args.user_agent})

def save_image(url, filename):
    response = session.get(url)
    if response.status_code != 200:
        print(f'{url} [{response.status_code}]')
        return
    path = filename
    if args.prefix is not None:
        path = args.prefix + ' ' + path
    if args.directory is not None:
        path = os.path.join(args.directory, path)
    with open(path, 'wb') as out:
        size = out.write(response.content)
    print(f'{url} [{response.status_code}]', '->', f'{path} [{size} bytes]')

for url in args.url:
    response = session.get(url)
    if response.status_code != 200:
        print(f'{url} [{response.status_code}]')
        continue
    for line in response.text.split('\n'):
        line = re.sub(r'\s+', ' ', line).strip()
        if not line.startswith('image : '):
            continue
        line = re.sub('^image : ', '', line).rstrip(',')
        data = json.loads(line)
        if 'album_images' in data:
            for image in data.get('album_images').get('images'):
                url = 'https://i.imgur.com/' + image['hash'] + image['ext']
                filename = data['hash'] + ' ' + image['hash'] + image['ext']
                save_image(url, filename)
        else:
            url = 'https://i.imgur.com/' + data['hash'] + data['ext']
            filename = data['hash'] + data['ext']
            save_image(url, filename)
