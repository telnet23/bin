#!/usr/bin/env python3

import sys
import urllib.parse

if 'encode' in sys.argv[0]:
    method = urllib.parse.quote
else:
    method = urllib.parse.unquote

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        print(method(arg))
else:
    for arg in sys.stdin:
        arg = arg.rstrip('\n')
        print(method(arg))
