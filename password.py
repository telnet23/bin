#!/usr/bin/env python3

import argparse
import datetime
import math
import os
import random
import sys

from decimal import Decimal

def c_range(a, b):
    return [chr(c) for c in range(ord(a), ord(b) + 1)]

def natural(value):
    if int(value) < 1:
        raise argparse.ArgumentTypeError('invalid choice: {} (choose from 1, 2, 3, ...)'.format(value))
    return int(value)

alphabets = {
    0: c_range('0', '9'),
    1: c_range('0', '9') + c_range('a', 'f'),
    2: c_range('0', '9') + c_range('a', 'z'),
    3: c_range('0', '9') + c_range('a', 'z') + c_range('A', 'Z'),
    4: c_range('0', '9') + c_range('a', 'z') + c_range('A', 'Z') +
        [ '_', '-' ],
    5: c_range('0', '9') + c_range('a', 'z') + c_range('A', 'Z') +
        [ '!', '"', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', '/',
          '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ')', '#' ]
}

parser = argparse.ArgumentParser(allow_abbrev=False, description='Generate random passwords.')
parser.add_argument('-c', '--complexity',
    type=int, choices=alphabets, default=3, action='store', help='password complexity')
parser.add_argument('-l', '--length',
    type=natural, default=32, action='store', help='password length')
parser.add_argument('-r', '--repeat',
    type=natural, default=1, action='store', help='number of passwords')
parser.add_argument('-w', '--write',
    type=str, action='store', help='write to file (use with care)')
args = parser.parse_args()

alphabet = alphabets[args.complexity]
permutations = len(alphabets[args.complexity]) ** args.length
per = ''
if args.repeat > 1:
    per = ' per password'
print('Permutations' + per + ': {:.3e}'.format(Decimal(permutations)), file=sys.stderr)
print('Entropy' + per + ': {:.0f} bits'.format(math.log(permutations) / math.log(2)), file=sys.stderr)
print(file=sys.stderr)

for i in range(0, args.repeat):
    if args.repeat != 1:
        print('{0:>{1}} '.format(i + 1, len(str(args.repeat))), end='')
    password = ''.join(random.choices(alphabet, k=args.length))
    print(password)

    if args.write is not None:
        with open(args.write, 'a') as f:
            print('[{}] {}'.format(datetime.datetime.now().isoformat(), password), file=f)
