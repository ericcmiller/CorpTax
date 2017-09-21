import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import numba
import ar1_approx as ar1

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *

'''
-------------------------------------------------------------------------
Discretizing state space for capital
-------------------------------------------------------------------------
dens   = integer, density of the grid: number of grid points between k and
         (1 - delta) * k
kstar  = scalar, capital stock choose w/o adjustment costs and mean
         productivity shock
kbar   = scalar, maximum capital stock the firm would ever accumulate
ub_k   = scalar, upper bound of capital stock space
lb_k   = scalar, lower bound of capital stock space
krat   = scalar, difference between upper and lower bound in log points
numb   = integer, the number of steps between the upper and lower bounds for
         the capital stock. The number of grid points is dens*numb.
K      = (sizek,) vector, grid points in the capital state space, from high
         to low
kvec  = (sizek,) vector, capital grid points
sizek = integer, the number of grid points in capital space
-------------------------------------------------------------------------
'''

# put in bounds here for the capital stock space
kstar = ((((1 / betafirm - 1 + delta) * ((alpha_l / w) **
                                         (alpha_l / (alpha_l - 1)))) /
         (alpha_k * (z[(sizez - 1) // 2] ** (1 / (1 - alpha_l))))) **
         ((1 - alpha_l) / (alpha_k + alpha_l - 1)))
kbar = 12#kstar * 500
lb_k = 0.001
ub_k = kbar
krat = np.log(lb_k / ub_k)
numb = np.ceil(krat / np.log(1 - delta))
K = np.empty(int(numb * dens))
for j in range(int(numb * dens)):
    K[j] = ub_k * (1 - delta) ** (j / dens)
kvec = K[::-1]
sizek = kvec.shape[0]
