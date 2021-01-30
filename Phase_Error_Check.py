import numpy as np
import scipy.linalg as lin
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import get_test_data

z_axis = np.linspace(0, 2e3, 1001).reshape(-1, 1)  # In Nanometers
wl_axis = np.linspace(198, 202, 11).reshape(-1, 1)  # In Nanometers

phi = np.pi/3 * 0 * np.ones(wl_axis.shape)
wafer_reflection = 0.25 * np.ones(wl_axis.shape)
mirror_reflection = 0.25 * np.ones(wl_axis.shape)
decoherence = 1 * np.ones(wl_axis.shape)

# interferogram_per_wl = wafer_reflection + mirror_reflection + 2 * np.sqrt(wafer_reflection * mirror_reflection) \
#      * decoherence(Z) * decoherence(NA) * decoherence(Tilt) * np.cos(phi + Z * 2 * np.pi / wl)

interferogram_matrix = wafer_reflection + mirror_reflection + 2 * np.sqrt(wafer_reflection * mirror_reflection) \
     * decoherence * np.cos(phi + (2 * np.pi / wl_axis) @ z_axis.reshape(1, -1))

diff_interferogram = np.mean(interferogram_matrix, 0) - interferogram_matrix[wl_axis.size//2, :]

# find the real phi/decoherence term from measured points


# plt.rcParams.update({'font.size': 24})
fig, ax = plt.subplots(2, 2)
# fig.dpi = 100
fig._tight = True

fig.axes[0].plot(wl_axis, interferogram_matrix[:, [0, 10, 20]], linewidth=2)
fig.axes[0].title._text = f'interferogram at Z = {z_axis[0, 0]:.0f}, {z_axis[10, 0]:.0f}, {z_axis[20, 0]:.0f}nm'
fig.axes[0].xaxis.label._text, fig.axes[0].yaxis.label._text = 'Wavelength', 'Intensity'

fig.axes[1].plot(z_axis, interferogram_matrix[[0, 1], :].transpose(), linewidth=2)
fig.axes[1].title._text = f'interferogram at min-max wl = {wl_axis[0, 0]:.0f}, {wl_axis[wl_axis.size//2, 0]:.0f}, {wl_axis[-1, 0]:.0f}nm'
fig.axes[1].xaxis.label._text, fig.axes[1].yaxis.label._text = 'Optical Path difference',  'Intensity'

fig.axes[2].plot(z_axis, diff_interferogram, linewidth=2)
fig.axes[2].title._text = f'diff interferogram, average vs wl = {wl_axis[wl_axis.size//2, 0]:.0f}nm'
fig.axes[2].xaxis.label._text, fig.axes[2].yaxis.label._text = 'Optical Path difference', 'Intensity'


[ax.grid() for ax in fig.axes]
# fig.axes[0].grid()
plt.get_current_fig_manager().window.showMaximized()
# plt.show()
