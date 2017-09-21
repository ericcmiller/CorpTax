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
Find model outputs given eq'm wage rate
------------------------------------------------------------------------
'''
op, e, l_d, y = get_firmobjects(w, z, kvec, alpha_k, alpha_l, delta, psi,
                            sizez, sizek)
VF, PF, optK, optI = VFI(e, betafirm, delta, kvec, Pi, sizez, sizek)
Gamma = find_SD(PF, Pi, sizez, sizek)
