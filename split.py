import json
import sys

src_path = sys.argv[1]
dst_path = sys.argv[2]

with open(src_path) as fp:
    src_data = json.load(fp)

k = 0
n = 100000
while src_data['features']:
    dst_data = {}
    for key in src_data.keys():
        if key == 'features':
            dst_data[key] = src_data[key][n * k:n * (k + 1)]
            src_data[key] = src_data[key][n * (k + 1):]
        else:
            dst_data[key] = src_data[key]
    k += 1
    with open(dst_path.replace('.', '-' + str(k) + '.'), 'w') as fp:
        json.dump(dst_data, fp)
