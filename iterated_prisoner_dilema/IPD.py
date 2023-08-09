import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import imageio
import os

def RDODE(X, t):
    w = 0.9
    b = 5
    c = 2
    A = np.array([[-c, -c, b*w - c], [0, 0, 0], [-c, -c*(1-w), b*w - c]])

    T, R, P, S = 5, 3, 1, 0.1
    m = 10
    c = 0.8

    A = np.array([[R*m, S*m, R*m], [T*m, P*m, T + P*(m - 1)], [R*m - c, S + P*(m - 1) - c, R*m - c]])

    x, y, z = X

    xdot = x * ((A @ X)[0] - np.dot(X, A @ X))
    ydot = y * ((A @ X)[1] - np.dot(X, A @ X))
    zdot = z * ((A @ X)[2] - np.dot(X, A @ X))

    return np.hstack((xdot, ydot, zdot))

def MRDODE(X, t):
    u = 1e-4

    T, R, P, S = 5, 4, 3, 2
    m = 10
    c = 0.5

    A = np.array([[R*m, S*m, R*m], [T*m, P*m, T + P*(m - 1)], [R*m - c, S + P*(m - 1) - c, R*m - c]])
    Q = np.array([[1-2*u, u, u], [u, 1-2*u, u], [u, u, 1 - 2*u]])

    x, y, z = X

    xdot = np.sum([X[i] * (A @ X)[i] * Q[i, 0] for i in range(3)]) - x * np.dot(X, A @ X)
    ydot = np.sum([X[i] * (A @ X)[i] * Q[i, 1] for i in range(3)]) - y * np.dot(X, A @ X)
    zdot = np.sum([X[i] * (A @ X)[i] * Q[i, 2] for i in range(3)]) - z * np.dot(X, A @ X)

    return np.hstack((xdot, ydot, zdot))

def plotOnSimplex(traj, j):
    f, ax = plt.subplots(1, 1)

    proj = np.array(
        [[-1 * np.cos(30 / 360 * 2 * np.pi), np.cos(30 / 360 * 2 * np.pi), 0],
         [-1 * np.sin(30 / 360 * 2 * np.pi), -1 * np.sin(30 / 360 * 2 * np.pi), 1]
         ])

    ts = np.linspace(0, 1, 10000)

    e1 = proj @ np.array([ts, 1 - ts, 0 * ts])
    e2 = proj @ np.array([0 * ts, ts, 1 - ts])
    e3 = proj @ np.array([ts, 0 * ts, 1 - ts])

    ax.plot(e1[0], e1[1], 'k-', alpha = 0.3)
    ax.plot(e2[0], e2[1], 'k-', alpha = 0.3)
    ax.plot(e3[0], e3[1], 'k-', alpha = 0.3)

    for i in range(traj.shape[2]):
        d = proj @ traj[:, :, i]
        ax.plot(d[0], d[1], '--', alpha=0.6)

    plt.axis('off')
    plt.savefig('IPDExpt/IPD'+str(j)+'.png')


if __name__ == '__main__':

    allSol = np.zeros((3, int(1e5) + 1, 10))

    os.mkdir('IPDExpt')

    for cInit in range(10):
        x0 = np.random.dirichlet(np.ones(3))
        t = np.linspace(0, int(1e4), int(1e5) + 1)
        sol = odeint(RDODE, x0, t)
        allSol[:, :, cInit] = sol.T
    
    [plotOnSimplex(allSol[:, :upTo, :], i) for i, upTo in enumerate(range(0, int(1e3) + 1, int(5)))]