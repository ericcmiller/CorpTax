import os

'''
------------------------------------------------------------------------
Investment by Firm Size
------------------------------------------------------------------------
'''

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *
from firm7_kspace import *
from firm7_geneq import *
from firm7_eqwage import *

# Plot investment rule as a function of firm size
# plt.figure()
fig, ax = plt.subplots()
ax.plot(kvec, optI[(sizez - 1) // 2, :]/kvec, 'k--', label='Investment rate')
ax.plot(kvec, np.ones(sizek)*delta, 'k:', label='Depreciation rate')
# Now add the legend with some customizations.
legend = ax.legend(loc='upper left', shadow=True)
# The frame is matplotlib.patches.Rectangle instance surrounding the legend.
frame = legend.get_frame()
frame.set_facecolor('0.90')
# Set the fontsize
for label in legend.get_texts():
    label.set_fontsize('large')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Size of Capital Stock')
plt.ylabel('Optimal Investment Rate')
plt.title('Policy Function, Investment - stochastic firm w/ adjustment ' +
          'costs')
output_path = os.path.join(output_dir, 'invest_firm7')
plt.savefig(output_path, dpi=200, bbox_inches="tight")
# plt.show()
plt.close()



# Plot the stationary distribution
fig, ax = plt.subplots()
ax.plot(kvec, Gamma.sum(axis=0))
plt.xlabel('Size of Capital Stock')
plt.ylabel('Density')
plt.title('Stationary Distribution over Capital')
output_path = os.path.join(output_dir, 'SD_k_firm7')
plt.savefig(output_path, dpi=200, bbox_inches="tight")
# plt.show()
plt.close()
