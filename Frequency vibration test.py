import numpy as np
import matplotlib.pyplot as plt

wl = np.array(np.linspace(235, 1000, 50))
kvec = 2*np.pi / wl

phase_err = kvec ** 3
phase_err = phase_err / np.mean(phase_err)

plt.plot(wl, phase_err)
plt.grid()
plt.show()


