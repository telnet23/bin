import random

from math import *

def sample(pmf):
    u = random.uniform(0, 1)
    x = 0
    cdf = pmf(x)
    while u > cdf:
        x += 1
        cdf += pmf(x)
    return x

def pmf(x):
    return exp(-3) * 3**x / factorial(x)

print([sample(pmf) for _ in range(100)])
