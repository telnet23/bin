import matplotlib.pyplot as plt
import numpy as np

#plt.rcParams['figure.dpi'] = 150

s = np.linspace(0, 100, 101)

payoffs = [
    ['Call',        [np.maximum(s-50, 0)]],
    ['Put',         [np.maximum(50-s, 0)]],
    ['Straddle',    [np.maximum(s-50, 0), np.maximum(50-s, 0)]],
    ['Strangle',    [np.maximum(s-67, 0), np.maximum(33-s, 0)]],
    ['Butterfly',   [np.maximum(s-67, 0), np.maximum(s-33, 0), -2*np.maximum(s-50, 0)]],
    ['Call Spread', [np.maximum(s-33, 0), -np.maximum(s-67, 0)]],
    ['Put Spread',  [np.maximum(67-s, 0), -np.maximum(33-s, 0)]],
]

fig, axs = plt.subplots(len(payoffs), 2, figsize=(4, 8))

for i in range(len(payoffs)):
    for j in range(2):
        if j == 0:
            axs[i, j].set_title('Long ' + payoffs[i][0])
        else:
            axs[i, j].set_title('Short ' + payoffs[i][0])
        whole = 0
        for component in payoffs[i][1]:
            if j == 0:
                component = -component
            whole += component
            #axs[i, j].plot(s, component)
        axs[i, j].plot(s, whole)
        axs[i, j].axis('equal')

fig.tight_layout()
fig.suptitle('Option Payoffs')
fig.subplots_adjust(top=0.92)
plt.show()
