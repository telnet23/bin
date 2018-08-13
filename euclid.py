import sys

a, b = int(sys.argv[1]), int(sys.argv[2])
n = 1
while b > 0:
    print(n, a, b)
    a, b = b, a % b
    n += 1
print('The GCD is', a)
