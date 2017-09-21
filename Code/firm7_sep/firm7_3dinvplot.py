import os

'''
------------------------------------------------------------------------
3D Investment Plot on Productivity and Optimal Capital Choice
------------------------------------------------------------------------
'''

from firm7_parameters import *
from firm7_functions import *
from firm7_zspace import *
from firm7_kspace import *
from firm7_geneq import *
from firm7_eqwage import *


# Stationary distribution in 3D
zmat, kmat = np.meshgrid(kvec, np.log(z))
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(kmat, zmat, Gamma, rstride=1, cstride=1, cmap=cm.coolwarm,
                linewidth=0, antialiased=False)
ax.view_init(elev=20., azim=20)  # to rotate plot for better view
ax.set_xlabel(r'Log Productivity')
ax.set_ylabel(r'Capital Stock')
ax.set_zlabel(r'Density')
output_path = os.path.join(output_dir, 'SD_3D_firm7')
plt.savefig(output_path)
# plt.show()
plt.close()
