import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy
from matplotlib import animation


# --- 2D BJT time simulation with finite difference method ---

N = 500
L = 100
t = 0.1

# Charge concentration and derivative

c = np.zeros((N, L, L))
n = np.zeros((N, L, L))
p = np.zeros((N, L, L))
V = np.zeros((N, L, L))

c[:, :, :] = 1
n[:, :, :] = 1
p[:, :, :] = 0.2
n[0, :, 45:55] = 0.2
n[1, :, 45:55] = 0.2
p[0, :, 45:55] = 1
p[1, :, 45:55] = 1

# pn junction
ehc = np.ones((L, L))
ehc[:, 35:65] = -1

static = np.ones((L, L))
static[0:35, 20:80] = 0


for i in range(1, N - 1):

    V[i + 1] = c[i] * (t**2) - V[i - 1] + 2 * V[i]

    Jn = n[i] * np.gradient(V[i]) + np.gradient(n[i])
    Jp = p[i] * np.gradient(V[i]) - np.gradient(n[i])

    n[i+1] = n[i] + t * np.sum(np.gradient(Jn))
    p[i+1] = p[i] + t * np.sum(np.gradient(Jp))

    c[i+1] = p[i+1] - n[i+1]


# Plotting and animation

fig = plt.figure()


def init():

    ax = sns.heatmap(c[0], square=True, cbar=False)
    ax.set(xticks=[], yticks=[], xlabel='x', ylabel='y')


def animate(i):

    ax = sns.heatmap(c[i], square=True, cbar=False)
    ax.set(xticks=[], yticks=[], xlabel='x', ylabel='y')


anim = animation.FuncAnimation(fig, animate, init_func=init, frames=20)

plt.show()
