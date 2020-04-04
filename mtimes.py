#!/usr/bin/env python3

import os

for root, directories, files in os.walk('.', topdown=False):
    if root.startswith('./Library'):
        continue
    times = set()
    times |= {os.path.getmtime(os.path.join(root, name)) for name in files}
    times |= {os.path.getmtime(os.path.join(root, name)) for name in directories}
    if not times:
        continue
    time = max(times)
    print(root + '  ' + str(round(time)))
    os.utime(root, (time, time))
