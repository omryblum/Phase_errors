import numpy as np
import matplotlib.pyplot as plt

theta_vec = np.array(np.linspace(0, np.pi/2, 100))
phi_vec = np.array(np.linspace(0, -np.pi/2, 100))

output_signal = []
for theta, phi in zip(theta_vec, phi_vec):
    input_signal = np.array([1, 1])
    polarizer_mat = np.array([[np.cos(theta)**2, np.cos(theta)*np.sin(theta)],
                              [np.cos(theta)*np.sin(theta), np.sin(theta)**2]])

    # # Sample = Mirror
    # sample_mat = np.array([[1, 0],
    #                        [0, 1]])
    # Sample = crazy ass target
    sample_mat = np.array([[0.7+0.2j, 0.2-0.1j],
                           [0.02+0.1j, 0.4]])

    analyzer_mat = np.array([[np.cos(phi)**2, np.cos(phi)*np.sin(phi)],
                             [np.cos(phi)*np.sin(phi), np.sin(phi)**2]])

    prior_sample_norm = (polarizer_mat @ input_signal) / np.linalg.norm(polarizer_mat @ input_signal)

    output_signal.append(analyzer_mat @ sample_mat @ prior_sample_norm)

output_signal = np.array(output_signal)
output_signal = np.linalg.norm(output_signal, axis=1)**2

plt.plot(theta_vec / np.pi * 180, output_signal)
plt.grid()
plt.xlabel('Rotation Pol [deg]')
plt.ylabel('Reflectivity')
plt.xticks([0, 45, 90], ['SS', 'X45', 'PP'])
plt.show()


