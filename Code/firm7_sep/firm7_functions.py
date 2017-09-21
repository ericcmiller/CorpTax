import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import numba
import ar1_approx as ar1

from firm7_parameters import *

'''
------------------------------------------------------------------------
Defined Functions:

VFI_loop
adj_costs
get_firmobjects
VFI
find_SD
GE_loop
get_L_s
------------------------------------------------------------------------
'''


@numba.jit
def VFI_loop(EV, e, cost, betafirm, Pi, sizez, sizek, Vmat):
    '''
    ------------------------------------------------------------------------
    This function loops over the state and control variables, operating on the
    value function to update with the last iteration's value function
    ------------------------------------------------------------------------
    INPUTS:
    EV       = (sizez, sizek) matrix, expected value function (expectations
               over z')
    e        = (sizez, sizek, sizek) matrix, cash flow values for each possible
               combination of capital stock today (state) and choice of capital
               stock tomorrow (control)
    cost     = (sizez, sizek, sizek) matrix, costly external finance values for
               each e.
    betafirm = scalar in [0, 1], the discount factor of the firm
    Pi       = (sizez, sizez) matrix, transition probabilities between points
               in the productivity state space
    sizez    = integer, number of grid points for firm productivity shocks
               state space
    sizek    = integer, the number of grid points in capital space
    Vmat     = (sizek, sizek) matrix, matrix with values of firm at each
               combination of state (k) and control (k')

    OTHER FUNCTIONS AND FILES CALLED BY THIS FUNCTION: None

    OBJECTS CREATED WITHIN FUNCTION: None

    FILES CREATED BY THIS FUNCTION: None

    RETURNS: Vmat
    ------------------------------------------------------------------------
    '''
    for i in range(sizez):  # loop over z
        for j in range(sizek):  # loop over k
            for m in range(sizek):  # loop over k'
                Vmat[i, j, m] = e[i, j, m] + cost[i,j,m] + betafirm * EV[i, m]

    return Vmat

@numba.jit
def adj_costs(kprime, k, delta, psi):
    '''
    -------------------------------------------------------------------------
    Compute adjustment costs
    -------------------------------------------------------------------------
    c   = (sizek, sizek) array, adjustment costs for each combination of
          combination of capital stock today (state), and choice of capital
          stock tomorrow (control)
    -------------------------------------------------------------------------
    '''
    c = (psi / 2) * (((kprime - ((1 - delta) * k)) ** 2) / k)

    return c

@numba.jit
def get_firmobjects(w, z, kvec, alpha_k, alpha_l, delta, psi, sizez, sizek):
    '''
    -------------------------------------------------------------------------
    Generating possible cash flow levels
    -------------------------------------------------------------------------
    op  = (sizez, sizek) matrix, operating profits for each point in capital
          stock and productivity shock grid spaces
    l_d = (sizez, sizek) matrix, firm labor demand for each point in capital
          stock and productivity shock grid spaces
    y   = (sizez, sizek) matrix, firm output for each point in capital
          stock and productivity shock grid spaces
    e   = (sizez, sizek, sizek) array, cash flow values for each possible
          combination of current productivity shock (state), capital stock
          today (state), and choice of capital stock tomorrow (control)
    -------------------------------------------------------------------------
    '''
    # Initialize arrays
    op = np.empty((sizez, sizek))
    l_d = np.empty((sizez, sizek))
    y = np.empty((sizez, sizek))
    e = np.empty((sizez, sizek, sizek))
    for i in range(sizez):
        for j in range(sizek):
            op[i, j] = ((1 - alpha_l) * ((alpha_l / w) **
                                         (alpha_l / (1 - alpha_l))) *
                        ((z[i] * (kvec[j] ** alpha_k)) **
                         (1 / (1 - alpha_l))))
            l_d[i, j] = (((alpha_l / w) ** (1 / (1 - alpha_l))) *
                         (z[i] ** (1 / (1 - alpha_l))) *
                         (kvec[j] ** (alpha_k / (1 - alpha_l))))
            y[i, j] = z[i] * (kvec[j] ** alpha_k) * (l_d[i, j] ** alpha_l)
            for m in range(sizek):
                e[i, j, m] = (op[i, j] - kvec[m] + ((1 - delta) * kvec[j]) -
                              adj_costs(kvec[m], kvec[j], delta, psi))

    return op, e, l_d, y

@numba.jit
def ex_finance(e,n0,n1):

    '''
    -------------------------------------------------------------------------
    Compute costs of external finance
    -------------------------------------------------------------------------
    Inputs:
    e  = (sizez, sizek, sizek) array, net cashflow for period.
    n0 = scalar, exogenous parameter representing the fixed cost of external
         finance.
    n1 = scalar, exogenous parameter representing the variable cost of external
         finance.

    Outputs:
    cost = (sizez, sizek, sizek) array, calculated external finance cost.
    -------------------------------------------------------------------------
    '''

    n0_func = lambda ec : n0 * np.all(ec > 0)

    cost = np.empty_like(e)
    for i in range(sizez):
        for j in range(sizek):
            for k in range(sizek):
                cost[i,j,k] = n0_func(e[i,j,k]) + n1 * np.clip(e[i,j,k], 0)
    return cost

def VFI(e, cost, betafirm, delta, kvec, Pi, sizez, sizek):
    '''
    ------------------------------------------------------------------------
    Value Function Iteration
    ------------------------------------------------------------------------
    VFtol     = scalar, tolerance required for value function to converge
    VFdist    = scalar, distance between last two value functions
    VFmaxiter = integer, maximum number of iterations for value function
    VFiter    = integer, current iteration number
    Vmat      = (sizez, sizek, sizek) array, array with values of firm at each
                combination of state (z, k) and control (k')
    Vstore    = (sizez, sizek, VFmaxiter) array, value function at each
                iteration of VFI
    V & TV    = (sizez, sizek) matrix, store the value function at each
                iteration (V being the most current value and TV the one prior)
    EV        = (sizez, sizek) matrix, expected value function (expectations
                over z')
    PF        = (sizez, sizek) matrix, indicies of choices (k') for all states
                (z, k)
    VF        = (sizez, sizek) matrix, matrix of value functions for each
                possible value of the state variables (k)
    ------------------------------------------------------------------------
    '''
    VFtol = 1e-6
    VFdist = 7.0
    VFmaxiter = 3000
    V = np.zeros((sizez, sizek))  # initial guess at value function
    Vmat = np.empty((sizez, sizek, sizek))  # initialize Vmat matrix
    Vstore = np.empty((sizez, sizek, VFmaxiter))  # initialize Vstore array
    VFiter = 1
    while VFdist > VFtol and VFiter < VFmaxiter:
        TV = V
        EV = np.dot(Pi, V)  # expected VF (expectation over z')
        Vmat = VFI_loop(EV, e, cost, betafirm, Pi, sizez, sizek, Vmat)

        Vstore[:, :, VFiter] = V.reshape(sizez, sizek)  # store value function
        # at each iteration for graphing later
        V = Vmat.max(axis=2)  # apply max operator to Vmat (to get V(k))
        PF = np.argmax(Vmat, axis=2)
        VFdist = (np.absolute(V - TV)).max()  # check distance between value
        # function for this iteration and value function from past iteration
        # print('VF iteration: ', VFiter)
        VFiter += 1

    #if VFiter < VFmaxiter:
    #    print('Value function converged after this many iterations:', VFiter)
    #else:
    #    print('Value function did not converge')

    VF = V  # solution to the functional equation

    '''
    ------------------------------------------------------------------------
    Find optimal capital and investment policy functions
    ------------------------------------------------------------------------
    optK = (sizez, sizek) vector, optimal choice of k' for each (z, k)
    optI = (sizez, sizek) vector, optimal choice of investment for each (z, k)
    ------------------------------------------------------------------------
    '''
    optK = kvec[PF]
    optI = optK - (1 - delta) * kvec

    return VF, PF, optK, optI


@numba.jit
def find_SD(PF, Pi, sizez, sizek):
    '''
    ------------------------------------------------------------------------
    Compute the stationary distribution of firms over (k, z)
    ------------------------------------------------------------------------
    SDtol     = tolerance required for convergence of SD
    SDdist    = distance between last two distributions
    SDiter    = current iteration
    SDmaxiter = maximium iterations allowed to find stationary distribution
    Gamma     = stationary distribution
    HGamma    = operated on stationary distribution
    ------------------------------------------------------------------------
    '''
    Gamma = np.ones((sizez, sizek)) * (1 / (sizek * sizez))
    SDtol = 1e-12
    SDdist = 7
    SDiter = 0
    SDmaxiter = 1000
    while SDdist > SDtol and SDmaxiter > SDiter:
        HGamma = np.zeros((sizez, sizek))
        for i in range(sizez):  # z
            for j in range(sizek):  # k
                for m in range(sizez):  # z'
                    HGamma[m, PF[i, j]] = \
                        HGamma[m, PF[i, j]] + Pi[i, m] * Gamma[i, j]
        SDdist = (np.absolute(HGamma - Gamma)).max()
        Gamma = HGamma
        SDiter += 1

    #if SDiter < SDmaxiter:
    #    print('Stationary distribution converged after this many iterations: ',
#              SDiter)
   # else:
   #     print('Stationary distribution did not converge')

    # Check if state space is binding
    #if Gamma.sum(axis=0)[-1] > 0.002:
    #    print('Stationary distribution is binding on k-grid.  Consider ' +
           #   'increasing the upper bound.')

    return Gamma


def GE_loop(w, *args):
    alpha_k, alpha_l, delta, betafirm, kvec, z, Pi, sizek, sizez, h = args
    op, e, l_d, y = get_firmobjects(w, z, kvec, alpha_k, alpha_l, delta, psi,
                                    sizez, sizek)
    cost = ex_finance(e, n0, n1)
    VF, PF, optK, optI = VFI(e, cost, betafirm, delta, kvec, Pi, sizez, sizek)
    Gamma = find_SD(PF, Pi, sizez, sizek)
    L_d = (Gamma * l_d).sum()
    Y = (Gamma * y).sum()
    I = (Gamma * optI).sum()
    Psi = (Gamma * adj_costs(optK, kvec, delta, psi)).sum()
    C = Y - I - Psi
    L_s = get_L_s(w, C, h)
    #print('Labor demand and supply = ', L_d, L_s)
    MCdist = L_d - L_s

    return MCdist


def get_L_s(w, C, h):
    L_s = w / (h * C)

    return L_s
