import random

counts = dict()
for trial in range(10000):
    if trial % 100 == 0:
        print('trial', trial)
    for N in range(1, 50+1):
        for n in range(1, N+1):
            seen = set()
            count = 0
            while len(seen) < N:
                seen |= set(random.sample(range(0, N), n))
                count += 1
            if (N, n) not in counts:
                counts[(N, n)] = list()
            counts[(N, n)].append(count)
with open('wash_data.tsv', 'w') as data:
    for N, n in counts:
        average = sum(counts[(N, n)]) / len(counts[(N, n)])
        line = '\t'.join(map(str, (N, n, average)))
        print(line, file=data)
        print(line)
