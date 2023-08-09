import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import imageio
import os


def RDODE(X, t):
    A = np.array([[2, 0], [0, 2]])
    B = np.array([[1, 0], [0, 7]])

    x, y = X

    xdot = x * ((A @ [y, 1-y])[0] - np.dot([x, 1-x], A @ [y, 1-y]))
    ydot = y * ((B.T @ [x, 1-x])[0] - np.dot([x, 1-x], B.T @ [y, 1-y]))

    return np.hstack((xdot, ydot))

def plotOnSimplex(traj, j):
    

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for i in range(traj.shape[2]):
        ax.plot(traj[0, :, i], traj[1, :, i])
    ax.set_xlabel('Probability of Player 1 Action 1')
    ax.set_ylabel('Probability of Player 2 Action 1')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    
    plt.savefig('MatchingPennies/'+str(j))
    
    
allSol = np.zeros((2, int(1e4) + 1, 10))

os.mkdir('MatchingPennies')

for cInit in range(10):
    x0 = np.random.rand(2)
    t = np.linspace(0, int(1e3), int(1e4) + 1)
    sol = odeint(RDODE, x0, t)
    allSol[:, :, cInit] = sol.T


[plotOnSimplex(allSol[:, :upTo, :], i) for i, upTo in enumerate(range(0, int(1e3) + 1, int(5)))]