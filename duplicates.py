#!/usr/bin/env python3

import csv
import hashlib
import os
import sys

checksums = {}

for arg in sys.argv[1:]:
    for root, directories, filenames in os.walk(arg):
        for filename in filenames:
            path = os.path.join(root, filename)
            if not os.path.isfile(path):
               continue
            with open(path, 'rb') as fil:
                content = fil.read()
                checksum = hashlib.md5(content).hexdigest()
            if checksum not in checksums:
                checksums[checksum] = set()
            checksums[checksum].add(path)
            print(checksum + '  ' + path, file=sys.stderr)

writer = csv.writer(sys.stdout)
for checksum, paths in checksums.items():
    if len(paths) < 2:
        continue
    #for i in range(len(paths)):
    #    if i == 0:
    #        print(checksum + '  ' + paths[i])
    #    else:
    #        print(' ' * len(checksum) + '  ' + paths[i])
    #print()
    for path in paths:
        writer.writerow([os.path.getsize(path), checksum, path])
