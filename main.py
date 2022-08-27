import numpy as np 
import matplotlib.pyplot as plt


# --- Helper Functions ---

def rot(deg: int) -> np.ndarray:

    return np.array([
        [np.cos(deg), np.sin(deg), 0, 0, 0, 0],
        [-np.sin(deg), np.cos(deg), 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, np.cos(deg), np.sin(deg), 0],
        [0, 0, 0, -np.sin(deg), np.cos(deg), 0],
        [0, 0, 0, 0, 0, 1]
    ]) 


# --- Defining the Element ---

A, L, E, I = 1, 1, 10, 10

# Using a line element with 2 nodes
K = np.array([
    [A*E/L, 0, 0, -A*E/L, 0, 0],
    [0, 12*E*I/L**3, 6*E*I/L**2, 0, -12*E*I/L**3, 6*E*I/L**2],
    [0, 6*E*I/L**2, 4*E*I/L, 0, -6*E*I/L**2, 2*E*I/L],
    [-A*E/L, 0, 0, A*E/L, 0, 0],
    [0, -12*E*I/L**3, -6*E*I/L**2, 0, 12*E*I/L**3, -6*E*I/L**2],
    [0, 6*E*I/L**2, 2*E*I/L, 0, -6*E*I/L**2, 4*E*I/L]
])

dof = 3


# --- Specifiying the Problem ---

n_elem = 3 # number of elements
n_nodes = 3

K_glob = np.zeros((dof*n_nodes, dof*n_nodes))

conns = np.array([
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0]
])

K_glob[:6, :6] = K
K_glob[-6:, -6:] = K@rot(60)

K_120 = K@rot(120)
K_glob[:3, :3] = K_120[:3, :3]
K_glob[:3, -3:] = K_120[:3, 3:]
K_glob[-3:, :3] = K_120[3:, :3]
K_glob[-3:, -3:] = K_120[3:, 3:]

F = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0])

u0 = np.array([0, 0, 0, L, 0, 0, L/2, -L*np.sin(60), 0])


# --- Visualisation ---

def plot_mesh(u, c):

    x = list(u[0::3])
    y = list(u[1::3])

    # Draw line back to the first point
    x.append(u[0])
    y.append(u[1])

    plt.plot(x, y, '-o', color=c)


plot_mesh(u0, 'r')
plot_mesh(u0 + np.linalg.solve(K_glob, F), 'b')
plot_mesh(u0 + np.linalg.solve(K_glob, 2*F), 'g')

plt.show()
