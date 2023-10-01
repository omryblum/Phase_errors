import numpy as np
import matplotlib.pyplot as plt

polarizer_vec = np.linspace(-np.pi/2, np.pi/2, 100)
analizer_vec = np.linspace(-np.pi/2, np.pi/2, 100)

# Sample = Mirror
# sample_mat = np.array([[1, 0],
#                        [0, 1]])
# Sample = random
sample_mat = np.random.random([2, 2]) + 1j*np.random.random([2, 2])
# Sample = crazy ass target
# sample_mat = np.array([[0.7 + 0.2j, 0.2 - 0.1j],
#                        [0.02 + 0.1j, 0.4]])

output_signal = np.zeros([polarizer_vec.shape[0], analizer_vec.shape[0]])
input_signal = np.array([1, 1])
for pol_ind, pol in enumerate(polarizer_vec):
    polarizer_mat = np.array([[np.cos(pol) ** 2, np.cos(pol) * np.sin(pol)],
                              [np.cos(pol) * np.sin(pol), np.sin(pol) ** 2]])
    prior_sample_norm = (polarizer_mat @ input_signal) / np.linalg.norm(polarizer_mat @ input_signal)

    for ana_ind, ana in enumerate(analizer_vec):
        analyzer_mat = np.array([[np.cos(ana)**2, np.cos(ana)*np.sin(ana)],
                                 [np.cos(ana)*np.sin(ana), np.sin(ana)**2]])

        output_signal[pol_ind][ana_ind] = np.linalg.norm(analyzer_mat @ sample_mat @ prior_sample_norm)**2

fig, ax = plt.subplots()
# xx, yy = np.meshgrid(polarizer_vec/np.pi*180, analizer_vec/np.pi*180)
# pl = ax.pcolor(xx, yy, output_signal)
# fig.colorbar(pl, ax=ax)
pl = ax.imshow(output_signal)
fig.colorbar(pl, ax=ax)
ax.grid(), ax.axis('equal')
xticks = np.round(np.linspace(0, analizer_vec.size-1, 5)).astype('int')
ax.set_xticks(xticks, np.round(analizer_vec[xticks]/np.pi*180))
yticks = np.round(np.linspace(0, polarizer_vec.size-1, 5)).astype('int')
ax.set_yticks(yticks, np.round(polarizer_vec[yticks]/np.pi*180))
ax.set_xlabel('Analyzer angle [deg]')
ax.set_ylabel('Polarizer angle [deg]')

plt.show()



