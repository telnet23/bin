#!/usr/bin/env python3

import os


def max_mtime(time, path):
    if os.path.basename(path) in {'.localized', '.DS_Store'}:
        return time
    try:
        return max(time or 0, os.path.getmtime(path))
    except (FileNotFoundError, PermissionError):
        return time


for root, directories, files in os.walk('.', topdown=False):
    if root.startswith('./Library'):
        continue
    time = None
    for name in files:
        time = max_mtime(time, os.path.join(root, name))
    for name in directories:
        time = max_mtime(time, os.path.join(root, name))
    if time is None:
        continue
    os.utime(root, (time, time))
    print(f'{time:.0f} {root}')
