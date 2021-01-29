import numpy as np
import scipy.linalg as lin
import matplotlib.pyplot as plt

z_axis = np.array(np.linspace(-10e3, 10e3, 100))  # In Nanometers
wl_axis = np.array(np.linspace(190, 1000, 100))  # In Nanometers

phi = np.pi/3
simple_cos = np.cos(phi + z_axis * (2 * np.pi / wl_axis[0]))

wafer_reflection = np.ones(wl_axis.shape)
mirror_reflection = 0.5 * np.ones(wl_axis.shape)
decoherence = 1

# interferogram_per_wl = wafer_reflection + mirror_reflection + 2 * np.sqrt(wafer_reflection * mirror_reflection) \
#      * decoherence(Z) * decoherence(NA) * decoherence(Tilt) * np.cos(phi + Z * 2 * np.pi / wl)

interferogram_matrix = wafer_reflection + mirror_reflection + 2 * np.sqrt(wafer_reflection * mirror_reflection) \
     * decoherence * np.cos(phi + z_axis[z_axis.shape[0]//2 + 2] * 2 * np.pi / wl_axis)


plt.rcParams.update({'font.size': 24})
fig, ax = plt.subplots(2, 2)
fig.dpi = 400
fig._tight = True

fig.axes[0].plot(wl_axis, interferogram_matrix, linewidth=3)
fig.axes[0].grid()
# fig.axes[0]=('interferogram across single Z'), plt.xlabel('Wavelength'), plt.ylabel('Intensity')
plt.get_current_fig_manager().window.showMaximized()
# plt.show
