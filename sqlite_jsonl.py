#!/usr/bin/env python3

import argparse
import json
import re
import sqlite3

parser = argparse.ArgumentParser()
parser.add_argument('input', action='store')
parser.add_argument('command', action='store')
args = parser.parse_args()

db = sqlite3.connect(f'file:{args.input}?mode=ro', uri=True)
cursor = db.execute(args.command)
for row in cursor:
    header = [description[0] for description in cursor.description]
    dictionary = {}
    for index in range(len(row)):
        if type(row[index]) is bytes:
            dictionary[header[index]] = row[index].decode('utf-8', 'ignore')
        else:
            dictionary[header[index]] = row[index]
    print(json.dumps(dictionary, separators=(',', ':'), sort_keys=True))
