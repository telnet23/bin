import math
import random
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

X, Y, Z = [], [], []

for _ in range(1000):
    ρ = random.uniform(0, 1)
    θ = random.uniform(0, 2 * math.pi)
    φ = random.uniform(0, math.pi)

    x = ρ * math.cos(θ) * math.sin(φ)
    y = ρ * math.sin(θ) * math.sin(φ)
    z = ρ * math.cos(φ)

    X.append(x)
    Y.append(y)
    Z.append(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X, Y, Z)
plt.show()
