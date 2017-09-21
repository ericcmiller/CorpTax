import os

'''
------------------------------------------------------------------------
Firm Size by Productivity
------------------------------------------------------------------------
'''

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *
from firm7_kspace import *
from firm7_geneq import *
from firm7_eqwage import *

# Plot investment rule as a function of productivity
# plt.figure()
fig, ax = plt.subplots()
ind = np.argmin(np.absolute(kvec - kstar))  # find where kstar is in grid
ax.plot(z, optI[:, ind - dens * 5] / kvec[ind - dens * 5], 'k', label='k = ' +
        str(kvec[ind - dens * 5]))
ax.plot(z, optI[:, ind] / kvec[ind], 'k:', label='k = ' + str(kvec[ind]))
ax.plot(z, optI[:, ind + dens * 5] / kvec[ind + dens * 5], 'k--', label='k = '
        + str(kvec[ind + dens * 5]))
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')
# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Productivity')
plt.ylabel('Optimal Investment Rate')
plt.title('Policy Function, Investment - stochastic firm w/ adjustment ' +
          'costs')
output_path = os.path.join(output_dir, 'invest_z_firm7')
plt.savefig(output_path, dpi=200, bbox_inches="tight")
# plt.show()
plt.close()


# Plot the stationary distribution
fig, ax = plt.subplots()
ax.plot(np.log(z), Gamma.sum(axis=1))
plt.xlabel('Productivity')
plt.ylabel('Density')
plt.title('Stationary Distribution over Productivity')
output_path = os.path.join(output_dir, 'SD_z_firm7')
plt.savefig(output_path, dpi=200, bbox_inches="tight")
# plt.show()
plt.close()
