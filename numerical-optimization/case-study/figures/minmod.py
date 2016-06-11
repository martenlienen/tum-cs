#!/usr/bin/env python

import math

import matplotlib.pyplot as pp
import numpy as np

deltax = 1


def minmod(a, b, c):
    """The minmod limiter."""
    if a * b < 0 or b * c < 0:
        return 0
    else:
        return math.copysign(min(abs(a), abs(b), abs(c)), a)


def centralize(X):
    """Translate linspace X such that its center is 0."""
    return X - X[0] - (X[-1] - X[0]) / 2


def evalpoly(P, X):
    """Evaluate polynomial P on X."""
    return np.dot(np.vstack([X**i for i in range(P.shape[0])]).T, P)


def plotpoly(P, X, **kwargs):
    """Plot polynomial P on X."""
    Y = evalpoly(P, centralize(X))

    pp.plot(X, Y, **kwargs)


def fillpoly(P, X, **kwargs):
    Y = evalpoly(P, centralize(X))

    pp.fill_between(X, 0, Y, **kwargs)


def plotminmod(P):
    P0, P1, P2 = P
    c00 = P0[0]
    c10 = P1[0]
    c20 = P2[0]
    ctilde = minmod(P1[1], (c20 - c10) / deltax, (c10 - c00) / deltax)
    active = P1[1] != ctilde

    n = 100
    X0 = np.linspace(-1, 0, n)
    X1 = np.linspace(0, 1, n)
    X2 = np.linspace(1, 2, n)

    # Plot areas
    fillpoly(P0, X0, hatch="/", facecolor="white")
    fillpoly(P1, X1, hatch="\\", facecolor="white")
    fillpoly(P2, X2, hatch="/", facecolor="white")

    if active and ctilde != 0:
        # Plot means
        plotpoly(P0[0:1], X0, color="k", ls="--", lw=2)
        plotpoly(P2[0:1], X2, color="k", ls="--", lw=2)

    # Plot limited slope
    plotpoly(np.array([P[1, 0], ctilde]), X1, lw=3, color="k")

    ax = pp.gca()
    for sp in ["left", "top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.xaxis.set_ticks([-1, 0, 1, 2])
    ax.xaxis.set_ticks_position("bottom")
    ax.yaxis.set_visible(False)

    pp.gcf().set_size_inches(3, 3)


def main():
    P = np.array([[1, 1], [1.6, 1.8], [2.75, 0.8]])
    plotminmod(P)
    pp.savefig("minmod-a.eps")
    pp.clf()

    P = np.array([[1.2, 1.2], [2.5, 0.9], [1.4, -1.25]])
    plotminmod(P)
    pp.savefig("minmod-b.eps")
    pp.clf()

    P = np.array([[1, 0.8], [1.5, -0.4], [1.9, 0.65]])
    plotminmod(P)
    pp.savefig("minmod-c.eps")
    pp.clf()


if __name__ == "__main__":
    main()
