import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import numba
import ar1_approx as ar1

from firm7_parameters import *
from firm7_functions import *

'''
-------------------------------------------------------------------------
Discretizing state space for productivity shocks
-------------------------------------------------------------------------
sigma_z   = scalar, standard deviation of ln(z)
num_sigma = scalar, number of standard deviations around mean to include in
            grid space for z
step      = scalar, distance between grid points in the productivity state
            space
Pi        = (sizez, sizez) matrix, transition probabilities between points in
            the productivity state space
z         = (sizez,) vector, grid points in the productivity state space
-------------------------------------------------------------------------
'''
# We will use the Rouwenhorst (1995) method to approximate a continuous
# distribution of shocks to the AR1 process with a Markov process.
sigma_z = sigma_eps / ((1 - rho ** 2) ** (1 / 2))
num_sigma = 3
step = (num_sigma * sigma_z) / (sizez / 2)
Pi, z = ar1.rouwen(rho, mu, step, sizez)
Pi = np.transpose(Pi)  # make so rows are where start, columns where go
z = np.exp(z)  # because the AR(1) process was for the log of productivity
