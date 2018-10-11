from collections import defaultdict

def factor(n):
    factors = defaultdict(int)
    m = 2
    while m ** 2 <= n:
        if n % m == 0:
            factors[m] += 1
            n = n // m
            m = 2
        else:
            m += 1
    if n > 0:
        factors[n] += 1
    return factors

for n in range(1, 1000+1):
    print({n: dict(factor(n))})
