#!/usr/bin/env python3

import sys
import urllib.parse

for arg in sys.argv[1:]:
    print(urllib.parse.unquote(arg))
