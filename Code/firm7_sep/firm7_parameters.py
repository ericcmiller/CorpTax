'''
------------------------------------------------------------------------
Specify Parameters
------------------------------------------------------------------------
beta      = scalar in (0, 1), rate of time preference
alpha_k   = scalar in [0, 1], exponent on capital in firm production function
alpha_l   = scalar in [0, 1], exponent on labor in firm production function
delta     = scalar in [0, 1], depreciation rate on capital
psi       = scalar, coefficient in quadratic adjustment costs for capital
w         = scalar, exogenous wage rate
r         = scalar, risk free interest rate, in eqm, r = (1 / beta) - 1
beta_firm = scalar in [0, 1], the discount factor of the firm
sigma_eps = scalar > 0, standard deviation of profit/productivity shocks to
            AR(1) process for firm productivity
mu        = scalar, unconditional mean of productivity shocks
rho       = scalar in [0, 1], persistence of productivity shocks
sizez     = integer, number of grid points for firm productivity shocks state
            space
dens      = density of the capital grid
------------------------------------------------------------------------
'''

# Household parameters
beta = 0.96
h = 6.616

# Firm parameters
alpha_k = 0.29715
alpha_l = 0.65
delta = 0.154
psi = 1.08
mu = 0
rho = 0.7605
sigma_eps = 0.213

# Factor prices
w = 1.3
r = ((1 / beta) - 1)
betafirm = (1 / (1 + r))

# state space parameters
sizez = 9
dens = 5

# External finance parameters
n0 = 0.08
n1 = 0.28
