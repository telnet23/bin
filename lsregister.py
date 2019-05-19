import json
import subprocess

types = {}
binary = '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister'
stdout = subprocess.run([binary, '-dump'], stdout=subprocess.PIPE).stdout
for section in stdout.decode('utf-8').split('-' * 80):
    section = section.strip()
    handler = {}
    for line in section.split('\n'):
        line = line.strip()
        try:
            key, value = line.split(':')
        except ValueError:
            continue
        key = key.strip()
        value = value.strip()
        if key == 'all roles':
            value = value.split(' (')[0]
        handler[key] = value
    if 'content type' in handler and 'all roles' in handler:
        types[handler['content type']] = handler['all roles']
print(json.dumps(types, indent=4, sort_keys=True))
