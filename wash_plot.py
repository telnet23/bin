from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

Ns, ns, xs = [], [], []
with open('wash_data.tsv') as data:
    for line in data:
        N, n, x = line.strip().split('\t')
        Ns.append(int(N))
        ns.append(int(n))
        xs.append(float(x))
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(Ns, ns, xs)
ax.set_xlabel('N')
ax.set_ylabel('n')
ax.set_zlabel('x')
plt.show()
