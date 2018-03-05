for k in range(32, 127 + 1):
    print('{:3} {}'.format(k, chr(k)), end='')
    if (k + 1) % 8 == 0:
        print()
    else:
        print(4 * ' ', end='')
