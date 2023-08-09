import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

def initialiseRandomVectors(dim, nInit):
    pX = np.random.dirichlet(np.ones(dim), size=(nInit)).T
    qY = np.random.dirichlet(np.ones(dim), size=(nInit)).T

    return pX, qY

def simulate(x0, G, nIterStart, nIter):
    A, B = G
    pX, qY = x0[0][:, -1], x0[1][:, -1]

    dim = np.shape(pX)[0]

    allPX = np.zeros((dim, nIter))
    allQY = np.zeros((dim, nIter))

    erX, erY = pX.T @ A @ qY, pX.T @ B @ qY
    allerX, allerY = np.zeros(nIter), np.zeros(nIter)

    for m, n in enumerate(range(nIterStart + 1, nIterStart + int(nIter) + 1)):
        eX, eY = np.zeros(dim), np.zeros(dim)
        brX, brY = np.argmax(A @ qY), np.argmax(pX.T @ B)
        eX[brX] = 1
        eY[brY] = 1

        pX = (n * pX + eX) / (n + 1)
        qY = (n * qY + eY) / (n + 1)

        allPX[:, m] = pX
        allQY[:, m] = qY

        erX = (n * erX + (pX.T @ A @ qY)) / (n + 1)
        erY = (n * erY + (pX.T @ B @ qY)) / (n + 1)

        allerX[m] = erX
        allerY[m] = erY

    return allPX, allQY

def plotOn3Simplex(trajX, trajY, j, nInit=1):
    fig = plt.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    proj = np.array(
        [[-1 * np.cos(30 / 360 * 2 * np.pi), np.cos(30 / 360 * 2 * np.pi), 0],
         [-1 * np.sin(30 / 360 * 2 * np.pi), -1 * np.sin(30 / 360 * 2 * np.pi), 1]
         ])

    ts = np.linspace(0, 1, 10000)

    e1 = proj @ np.array([ts, 1 - ts, 0 * ts])
    e2 = proj @ np.array([0 * ts, ts, 1 - ts])
    e3 = proj @ np.array([ts, 0 * ts, 1 - ts])

    ax1.plot(e1[0], e1[1], 'k', alpha=0.6)
    ax1.plot(e2[0], e2[1], 'k', alpha=0.6)
    ax1.plot(e3[0], e3[1], 'k', alpha=0.6)

    ax2.plot(e1[0], e1[1], 'k', alpha=0.6)
    ax2.plot(e2[0], e2[1], 'k', alpha=0.6)
    ax2.plot(e3[0], e3[1], 'k', alpha=0.6)

    for i in range(nInit):
        d = proj @ trajX[:, i, :]
        ax1.plot(d[0], d[1], '--')
        ax1.scatter(d[0, -1], d[1, -1], marker='+')

        d = proj @ trajY[:, i, :]
        ax2.plot(d[0], d[1], '--')
        ax2.scatter(d[0, -1], d[1, -1], marker='+')

    plt.savefig('ShapleyExpt/Shapley' + str(j) + '.png')


def plotOn2Simplex(trajX, trajY, j, nInit=1):
    f, ax = plt.subplots(1, 1)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])

    for i in range(nInit):
        ax.plot(trajX[0, i, :], trajY[0, i, :])
        ax.scatter(trajX[0, i, -1], trajY[0, i, -1], marker='+')

    plt.savefig('IPDExpt/IPD' + str(j) + '.png')


if __name__ == "__main__":
    dim = 3
    nIter = int(1e5)
    nInit = 10
    beta = 0

    allInitX, allInitY = np.zeros((dim, nIter, nInit)), np.zeros((dim, nIter, nInit))

    T, R, P, S = 5, 4, 3, 2
    m = 10
    c = 0.5

    # A = np.array([[R * m, S * m, R * m], [T * m, P * m, T + P * (m - 1)], [R * m - c, S + P * (m - 1) - c, R * m - c]])
    # B = -A
    # A = np.array([[1, -1], [-1, 1]])
    # B = -A
    A = np.array([[1, 0, beta], [beta, 1, 0], [0, beta, 1]])
    B = np.array([[-beta, 1, 0], [0, -beta, 1], [1, 0, -beta]])
    G = (A, B)
    for cInit in tqdm(range(nInit)):

        x0 = initialiseRandomVectors(dim, 1)

        allPX, allQY = simulate(x0, G, 0, nIter)
        allInitX[:, :, cInit] = allPX
        allInitY[:, :, cInit] = allQY


    [plotOn3Simplex(allInitX.transpose((0, 2, 1))[:, :, :upTo], allInitY.transpose((0, 2, 1))[:, :, :upTo], j, nInit) for j, upTo in enumerate(range(0, int(1e3) + 1, 5))]
