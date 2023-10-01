import numpy as np
import matplotlib.pyplot as plt

# What free parameters in the problem?
# Per Wavelength,
#   There is 1 POI and may be more than 1 periphery, so may be several R per wl
#   change is Z should grab additional energy rings and reduce average power,
#   same Z behaviour for all wavelength but with offset of smallest pad position

# Number of free parameters: 2n*wl (reflectivity) + n*Zpoints (energy) + wl (offset) --> (2n+1)*wl + n*Zpoints
# Number of datapoints: wl*Zpoints
# wl*Zpoints >> (2n+1)*wl + n*Zpoints   -->   Zpoints >> 2n+1   -->   Zpoints ~ 50
# This means complex energy distribution for enlarged pad cannot be solved for a single independent wl

R_in = 1
R_out = 0.5
delta_phi = 1

pad = np.zeros([100, 100])
pad[40:60, 35:65] = 1
marked_illum = pad.copy()

radius_vec = np.arange(1, 20)
illum_center = np.array([52, 52])

xvec = np.arange(0, 100)
yvec = np.arange(0, 100)

c1 = np.zeros(radius_vec.shape)
c2 = np.zeros(radius_vec.shape)
for radius in radius_vec:
    energy_list = []
    for xloc in xvec:
        for yloc in yvec:
            if (xloc - illum_center[0])**2 + (yloc - illum_center[0])**2 < radius**2:
                marked_illum[xloc, yloc] = 2
                energy_list.append(pad[xloc, yloc])
    c1[radius-1] = np.count_nonzero(np.round(energy_list)==1)
    c2[radius-1] = np.count_nonzero(np.round(energy_list)==0)

c1c2 = c1+c2
c1 = c1/c1c2
c2 = c2/c1c2

I = c1*R_in + c2*R_out + 2*np.cos(delta_phi)*(c1*c2*R_in*R_out)**0.5

# fig, ax = plt.subplots()
# pl = ax.imshow(marked_illum)
# fig.colorbar(pl, ax=ax)
# ax.grid(), ax.axis('equal')
# plt.show()

fig, ax = plt.subplots(3,1)
ax[0].plot(radius_vec*2, c1)
ax[1].plot(radius_vec*2, c2)
ax[2].plot(radius_vec*2, I)

# ax.grid(), ax.axis('equal')
ax[2].set_xlabel('illumination diameter')
ax[2].set_ylabel('measured intensity')
ax[0].set_title('20X30um pad simulated scan in Z')

plt.show()



