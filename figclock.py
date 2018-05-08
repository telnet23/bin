#!/usr/bin/env python3

# ./figclock.py
# ./figclock.py -c='figlet -f Roman %-I:%M' -d=../figlet-fonts -fs=2
# ./figclock.py -c='figlet -f Spliff %H:%M:%S' -d=../figlet-fonts -x=center -y=center
# ./figclock.py -c='figlet -f banner %H:%M:%S' -d=../figlet-fonts -o=backward

import argparse
import os
import random
import signal
import subprocess
import sys
import time

parser = argparse.ArgumentParser(description='FIGclock - FIGlet Clock and Screensaver')
parser.add_argument('-c', '--command', action='store', \
    default='figlet -f banner %H:%M:%S', type=str, \
    help='command to obtain output from, passed through strftime first \
        (default: %(default)s)')
parser.add_argument('-cs', '--character-sleep', action='store', \
    default=0.001, metavar='SECONDS', type=float, \
    help='number of seconds to sleep for after each character is printed (default: %(default)s)')
parser.add_argument('-d', '--directory', action='store', \
    metavar='PATH', type=str, \
    help='working directory (default: current working directory)')
parser.add_argument('-fs', '--frame-sleep', action='store', \
    default=1, metavar='SECONDS', type=float, \
    help='number of seconds to sleep for after each frame is printed (default: %(default)s)')
parser.add_argument('-o', '--order', action='store', \
    choices=['forward', 'backward', 'random'], default='random', \
    help='order in which characters are printed (default: %(default)s)')
parser.add_argument('-v', '--over', action='store_true', \
    help='print each frame over the previous frame (default: %(default)s)')
parser.add_argument('-x', '--x-offset', action='store', metavar='COLUMNS', \
    choices=['left', 'center', 'right', 'random'], default='random', \
    help='number of columns by which frame is offset (default: %(default)s)')
parser.add_argument('-y', '--y-offset', action='store', metavar='ROWS', \
    choices=['top', 'center', 'bottom', 'random'], default='random', \
    help='number of rows by which frame is offset (default: %(default)s)')
args = parser.parse_args()

if args.directory is not None:
    os.chdir(args.directory)

def sigint(*args):
    print2('\x1B[H', '\x1B[2J', '\x1B[?25h')
    sys.exit(0)
signal.signal(signal.SIGINT, sigint)
def print2(*args):
    print(''.join(args), end='', flush=True)
print2('\x1B[?25l') # Hide cursor

last = 0
while True:
    if time.time() - last < args.frame_sleep:
        time.sleep(0.001)  # 1 ms
        continue

    command = time.strftime(args.command, time.localtime(time.time() + 0.5)).split()
    output = subprocess.check_output(command).decode('utf-8').split('\n')

    frame = dict()
    y = -1
    x_max = 0
    for line in output:
        line = line.rstrip()
        if line == '':
            continue
        y += 1
        x = -1
        for char in line:
            x += 1
            if char != ' ':
                frame[(x, y)] = char
            if x > x_max:
                x_max = x

    width, height = os.get_terminal_size()

    if args.x_offset == 'left':
        x_offset = 0
    elif args.x_offset == 'center':
        x_offset = int((width - (x_max + 1))/2)
    elif args.x_offset == 'right':
        x_offset = width - (x_max + 1)
    elif args.x_offset == 'random':
        x_offset = random.randint(0, width - (x_max + 1))

    if args.y_offset == 'top':
        y_offset = 0
    elif args.y_offset == 'center':
        y_offset = int((height - (y + 1))/2)
    elif args.y_offset == 'bottom':
        y_offset = height - (y + 1)
    elif args.y_offset == 'random':
        y_offset = random.randint(0, height - (y + 1))

    if not args.over:
        print2('\x1B[2J')

    while frame:
        if args.order == 'forward':
            x_frame, y_frame = list(frame.keys())[0]
        elif args.order == 'backward':
            x_frame, y_frame = list(reversed(list(frame.keys())))[0]
        elif args.order == 'random':
            x_frame, y_frame = random.sample(list(frame.keys()), 1)[0]

        x, y = x_offset + x_frame + 1, y_offset + y_frame + 1
        print2('\x1B[', str(y), ';', str(x), 'H', frame[(x_frame, y_frame)])
        del(frame[(x_frame, y_frame)])
        time.sleep(args.character_sleep)

    last = time.time()
