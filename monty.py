from random import randrange
import time

start = time.time()

iterations    = 0
cars_switch   = 0
cars_noswitch = 0

doors = ['car', 'goat', 'goat']

while iterations < 1000000:
    iterations += 1

    choose = randrange(0, len(doors))
    reveal = 0

    while doors[reveal] == 'car' or reveal == choose:
        reveal += 1

    if doors[choose] == 'car':
        cars_noswitch += 1

    switch = 0

    while switch == reveal or switch == choose:
        switch += 1

    if doors[switch] == 'car':
        cars_switch += 1

print('Iterations                {}'.format(iterations))
print('Cars (with Switching)     {0} ({1})'.format(cars_switch, cars_switch / iterations))
print('Cars (without Switching)  {0} ({1})'.format(cars_noswitch, cars_noswitch / iterations))
print('Run Time                  {:.2f} seconds'.format(time.time() - start))
