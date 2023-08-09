import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def TuylsODE(X, t, G, agentParams):
    alpha, beta = agentParams
    A, B = G
    x, y = X[0:2], X[2:]
    xdot, ydot = np.zeros(2), np.zeros(2)

    xdot[0] = x[0] * alpha * beta * (((A @ y)[0] - np.dot(x, A @ y)) - (1/beta) * (np.log(x[0]) - np.dot(x, np.log(x))))
    xdot[1] = x[1] * alpha * beta * (((A @ y)[1] - np.dot(x, A @ y)) - (1 / beta) * (np.log(x[1]) - np.dot(x, np.log(x))))
    ydot[0] = y[0] * alpha * beta * (((x.T @ B)[0] - np.dot(x, B @ y)) - (1/beta) * (np.log(y[0]) - np.dot(y, np.log(y))))
    ydot[1] = y[1] * alpha * beta * (((x.T @ B)[0] - np.dot(x, B @ y)) - (1 / beta) * (np.log(y[1]) - np.dot(y, np.log(y))))

    return np.hstack((xdot, ydot))

def plotOn2Simplex(trajX, trajY, nInit=1):
    f, ax = plt.subplots(1, 1)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    for i in range(nInit):
        ax.plot(trajX[0, i, :], trajY[0, i, :])
        ax.scatter(trajX[0, i, -1], trajY[0, i, -1], marker='+')

    plt.show()

if __name__ == "__main__":
    dim = 2
    nIter = int(5e4)
    nInit = 10

    allSol = np.zeros((10 * nIter + 1, dim*2, nInit))
    A = np.array([[1, -1], [-1, 1]])
    B = -A
    G = (A, B)
    alpha = 0.1
    tau = 1
    agentParams = (alpha, tau)

    for cInit in range(nInit):
        x0 = np.random.dirichlet(np.ones(2), size=2).reshape(4)
        t = np.linspace(0, nIter, 10 * nIter + 1)
        sol = odeint(TuylsODE, x0, t, args=(G, agentParams))
        allSol[:, :, cInit] = sol

    plotOn2Simplex(allSol.transpose(1, 2, 0)[0:2], allSol.transpose(1, 2, 0)[2:], nInit)