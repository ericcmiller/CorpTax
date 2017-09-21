import os

'''
------------------------------------------------------------------------
Profits per Firm Size
------------------------------------------------------------------------
'''

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *
from firm7_kspace import *
from firm7_geneq import *
from firm7_eqwage import *

# Plot operating profits as a function of firm size
# plt.figure()
fig, ax = plt.subplots()
ax.plot(kvec, op[0, :], 'k--', label='z = ' + str(z[0]))
ax.plot(kvec, op[(sizez - 1) // 2, :], 'k:', label='z = ' + str(z[(sizez - 1)
                                                                // 2]))
ax.plot(kvec, op[-1, :], 'k', label='z = ' + str(z[-1]))
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
plt.ylabel('Operating Profits')
plt.title('Operating Profits as a Function of Firm Size')
output_path = os.path.join(output_dir, 'Profits_firm7')
plt.savefig(output_path, dpi=200, bbox_inches="tight")
# plt.show()
plt.close()
