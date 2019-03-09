import os
import sys

directories = sys.argv[1:]
if not directories:
    directories.append('.')
for directory in directories:
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        size = os.path.getsize(path)
        if size < 256:
            os.remove(path)
            print('rm', path, f'({size} bytes)')
