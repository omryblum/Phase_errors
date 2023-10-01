import numpy as np
import matplotlib.pyplot as plt


def plot_input_signals():
    # Plotting section inputs
    fig, ax = plt.subplots(2, 2)
    ax[0, 0].plot(all_wavelengths, system_raw_intensity)
    ax[0, 0].set_title('System raw intensity'), ax[0, 0].grid()
    ax[0, 0].set_xlabel('Wavelength [nm]'), ax[0, 0].set_ylabel('normalized intensity')

    lines = []
    lines.append(ax[0, 1].plot(z_scan_vec, decomposed_signal[0, :], label=all_wavelengths[0]))
    lines.append(ax[0, 1].plot(z_scan_vec, decomposed_signal[round(len(all_wavelengths)*1/3), :], label=round(all_wavelengths[round(len(all_wavelengths)*1/3)])))
    lines.append(ax[0, 1].plot(z_scan_vec, decomposed_signal[-1, :], label=all_wavelengths[-1]))
    ax[0, 1].set_title('Decomposed interferograms by wavelength'), ax[0, 1].grid()
    ax[0, 1].set_xlabel('Z scan position [nm]'), ax[0, 1].set_ylabel('normalized intensity')
    ax[0, 1].legend(labels=[x[0].get_label() for x in lines])

    lines = []
    lines.append(ax[1, 0].plot(all_wavelengths, decomposed_signal[:, round(len(z_scan_vec)*1/2)], label=round(z_scan_vec[round(len(z_scan_vec)*1/2)])))
    lines.append(ax[1, 0].plot(all_wavelengths, decomposed_signal[:, round(len(z_scan_vec)*2/3)], label=round(z_scan_vec[round(len(z_scan_vec)*2/3)])))
    lines.append(ax[1, 0].plot(all_wavelengths, decomposed_signal[:, -1], label=z_scan_vec[-1]))
    ax[1, 0].set_title('Decomposed interferograms, by Z position'), ax[1, 0].grid()
    ax[1, 0].set_xlabel('Wavelength [nm]'), ax[1, 0].set_ylabel('normalized intensity')
    ax[1, 0].legend(labels=[x[0].get_label() for x in lines])

    ax[1, 1].plot(z_scan_vec, WLI_signal)
    ax[1, 1].set_title('WLI signal'), ax[1, 1].grid()
    ax[1, 1].set_xlabel('Z scan position'), ax[1, 1].set_ylabel('normalized intensity')


def plot_estimator_signals():
    # Plotting section estimators
    fig, ax = plt.subplots(2, 2)
    lines = []
    lines.append(ax[0, 0].plot(all_wavelengths, system_raw_intensity, label='Original Intensity'))
    lines.append(ax[0, 0].plot(all_wavelengths, est_wafer_ref, label='Estimated intensity'))
    # lines.append(ax[0, 0].plot(est_wafer_ref, label='Estimated intensity'))
    ax[0, 0].set_title('System Intensity'), ax[0, 0].grid()
    ax[0, 0].set_xlabel('Wavelength [nm]'), ax[0, 0].set_ylabel('normalized intensity')
    ax[0, 0].legend(labels=[x[0].get_label() for x in lines])

    lines = []
    lines.append(ax[0, 1].plot(all_wavelengths, wafer_phase, label='Original Phase'))
    lines.append(ax[0, 1].plot(all_wavelengths, est_wafer_phase, label='Estimated Phase'))
    # lines.append(ax[0, 1].plot(est_wafer_phase, label='Estimated Phase'))
    ax[0, 1].set_title('System Phase'), ax[0, 1].grid()
    ax[0, 1].set_xlabel('Wavelength [nm]'), ax[0, 1].set_ylabel('phase')
    ax[0, 1].legend(labels=[x[0].get_label() for x in lines])

    #
    # ax[0, 1].plot(z_scan_est, est_wafer_ref)
    # ax[0, 1].set_title('Estimated raw intensity'), ax[0, 1].grid()
    # ax[0, 1].set_xlabel('Wavelength [nm]'), ax[0, 1].set_ylabel('normalized intensity')
    # #
    # lines = []
    # lines.append(ax[1, 0].plot(all_wavelengths, decomposed_signal[:, round(len(z_scan_vec)*2/3)], label=round(z_scan_vec[round(len(z_scan_vec)*2/3)])))
    # lines.append(ax[1, 0].plot(all_wavelengths, decomposed_signal[:, -1], label=z_scan_vec[-1]))
    # ax[1, 0].set_title('Decomposed interferograms, by Z position'), ax[1, 0].grid()
    # ax[1, 0].set_xlabel('Wavelength [nm]'), ax[1, 0].set_ylabel('normalized intensity')
    # ax[1, 0].legend(labels=[x[0].get_label() for x in lines])
    #
    # ax[1, 1].plot(z_scan_vec, WLI_signal)
    # ax[1, 1].set_title('WLI signal'), ax[1, 1].grid()
    # ax[1, 1].set_xlabel('Z scan position'), ax[1, 1].set_ylabel('normalized intensity')


# Base signal and inputs
all_wavelengths = np.linspace(300, 1100, 1000)
# system_raw_intensity = np.minimum(np.maximum(0, all_wavelengths-500)/200, np.abs(np.minimum(0, all_wavelengths-800)/100))
system_raw_intensity = np.zeros(all_wavelengths.shape)
system_raw_intensity[400:500] = 1
# wafer_reflectivity = np.ones(len(all_wavelengths))
# mirror_reflectivity = np.ones(len(all_wavelengths))
wafer_reflectivity = np.ones(len(all_wavelengths)) * system_raw_intensity
mirror_reflectivity = np.ones(len(all_wavelengths)) * system_raw_intensity
wafer_phase = 0 * np.ones(len(all_wavelengths))
z_scan_vec = 100000 * np.linspace(-1, 1, 100001) # 200um range at 800nm wl gives FWHM resolution of 4nm

# Estimation variables
estimation_wl = all_wavelengths
z_scan_est = z_scan_vec

# Creation of the separated signals per wl
decomposed_signal = np.outer(wafer_reflectivity + mirror_reflectivity, np.ones(len(z_scan_vec))) + \
                    np.outer(2*np.sqrt(wafer_reflectivity*mirror_reflectivity), np.ones(len(z_scan_vec))) * \
                    1 * np.cos(np.outer(2*np.pi/all_wavelengths, z_scan_vec) + np.outer(wafer_phase, np.ones(len(z_scan_vec))))

# Creation of WLI combined signal
WLI_signal = np.sum(decomposed_signal, 0)

# DFT on WLI signal for frequency decomposition
inner_vec = np.outer(2*np.pi/estimation_wl, z_scan_est)
# cosine = (np.cos(inner_vec) + 1j*np.sin(inner_vec)) / len(z_scan_est)
normed_cos = np.cos(inner_vec) / np.outer(np.sum(np.cos(inner_vec)**2, 1), np.ones(inner_vec.shape[1]))
normed_sin = np.sin(inner_vec) / np.outer(np.sum(np.sin(inner_vec)**2, 1), np.ones(inner_vec.shape[1]))

cosine = (normed_cos + 1j*normed_sin)
DCT_decomposition = cosine @ WLI_signal
# Normalization per frequency energy density?
DCT_decomposition = DCT_decomposition/all_wavelengths**2
# DCT_decomposition = np.fft.fftshift(np.fft.fft(WLI_signal))

print('total signal energy is %f', np.sum(np.abs(DCT_decomposition)))

est_wafer_ref = np.abs(DCT_decomposition) / max(np.abs(DCT_decomposition))  # normalizing intensity
est_wafer_phase = np.arctan2(np.imag(DCT_decomposition), np.real(DCT_decomposition))

# Recreation of signal WLI signal after compact support


# Correction of sampling points vector
plot_input_signals()
plot_estimator_signals()
plt.show()






