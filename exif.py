import os
import piexif
import sys

exif = piexif.load(sys.argv[1])
rows = []
pads = []
for ifd in sorted(exif):
    if ifd == 'thumbnail' or exif[ifd] is None:
        continue
    for tag in sorted(exif[ifd]):
        if ifd in piexif.TAGS and tag in piexif.TAGS[ifd]:
            name = piexif.TAGS[ifd][tag]['name']
        else:
            name = ''
        value = exif[ifd][tag]
        if type(value) is bytes:
            try:
                value = value.decode('utf-8')
            except UnicodeDecodeError:
                pass
        row = list(map(str, (ifd, tag, name, value)))
        rows.append(row)
        for i in range(len(row)):
            if i + 1 < len(pads):
                pads[i] = max(pads[i], len(row[i]))
            else:
                pads.append(len(row[i]))
for row in rows:
    print(f'{row[0]:<{pads[0]}}    {row[1]:>{pads[1]}}    {row[2]:<{pads[2]}}    {row[3]}')
