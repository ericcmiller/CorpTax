import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
import os
import numba
import ar1_approx as ar1
import time as time

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *
from firm7_kspace import *

'''
------------------------------------------------------------------------
Solve for general equilibrium
------------------------------------------------------------------------
'''
start_time = time.clock()
results = opt.bisect(GE_loop, 0.1, 2, args=(alpha_k, alpha_l, delta, betafirm,
                                            kvec, z, Pi, sizek, sizez, h),
                     xtol=1e-4, full_output=True)
print(results)
w = results[0]
GE_time = time.clock() - start_time
print('Solving the GE model took ', GE_time, ' seconds to solve')
print('SS wage rate = ', w)
