import math
import random
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

X, Y, Z = [], [], []

for _ in range(1000):
    x = random.uniform(0, 1)
    y = random.uniform(0, 1)
    z = random.uniform(0, 1)

    #rho = random.uniform(0, 1)
    #theta = random.uniform(0, 2*math.pi)
    #phi = random.uniform(0, math.pi)

    #x = rho * math.cos(theta) * math.sin(phi)
    #y = rho * math.sin(theta) * math.sin(phi)
    #z = rho * math.cos(phi)

    X.append(x)
    Y.append(y)
    Z.append(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
plt.show()
