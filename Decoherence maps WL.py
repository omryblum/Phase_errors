import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.core import argmax


# Gaussian weighting function
def gaussian_weights(wavelengths, center_wavelength, bandwidth):
    """
    Calculate Gaussian weights for the wavelengths.
    Parameters:
        wavelengths (np.ndarray): Array of wavelengths (in nanometers).
        center_wavelength (float): Central wavelength (in nanometers).
        bandwidth (float): Bandwidth of the Gaussian (in nanometers, FWHM).
    Returns:
        np.ndarray: Gaussian weights.
    """
    sigma = bandwidth / (2 * np.sqrt(2 * np.log(2)))  # Convert FWHM to standard deviation
    weights = np.exp(-((wavelengths - center_wavelength) ** 2) / (2 * sigma ** 2))
    return weights / np.sum(weights)  # Normalize the weights

# Function to calculate coherence parameter
def coherence_degradation_by_exp(wavelengths, weights, opd):
    """
    Calculate the coherence parameter degradation for a given OPD.
    Parameters:
        wavelengths (np.ndarray): Array of wavelengths (in nanometers).
        weights (np.ndarray): Gaussian weights for the wavelengths.
        opd (float): Optical path difference (in micrometers).
    Returns:
        float: Coherence parameter degradation.
    """
    phase = 2 * np.pi * opd * 1000 / wavelengths
    complex_sum = np.sum(weights * np.exp(1j * phase))

    coherence = np.abs(complex_sum)
    return coherence

# Function to calculate coherence parameter
def coherence_degradation_by_cosine(wavelengths, weights, opd):
    """
    Calculate the coherence parameter degradation for a given OPD.
    Parameters:
        wavelengths (np.ndarray): Array of wavelengths (in nanometers).
        weights (np.ndarray): Gaussian weights for the wavelengths.
        opd (float): Optical path difference (in micrometers).
    Returns:
        float: Coherence parameter degradation.
    """
    max_index = weights.argmax()
    phase = 2 * np.pi * opd * 1000 / wavelengths
    complex_sum = np.sum(weights * np.cos(phase-phase[max_index]))

    coherence = np.abs(complex_sum)
    return coherence

# Parameters
center_wavelengths = np.linspace(200, 1000, 100)  # Center wavelengths (200 nm to 1000 nm)
bandwidth = 4  # Fixed bandwidth (2 nm)
opd_values = np.linspace(0, 50, 100)           # OPD values (0 to 50000 nm)
num_wavelengths = 10000                          # Number of wavelength samples

# Generate wavelengths within the fixed bandwidth
fixed_bandwidth_wavelengths = np.linspace(
    center_wavelengths[0] - 2*bandwidth,
    center_wavelengths[-1] + 2*bandwidth,
    num_wavelengths
)

# Create a 2D grid for coherence parameter degradation
coherence_map = np.zeros((len(opd_values), len(center_wavelengths)))

# Calculate coherence degradation for each center wavelength and OPD
for i, central_wl in enumerate(center_wavelengths):
    # Gaussian weights for the current center wavelength
    weights = gaussian_weights(fixed_bandwidth_wavelengths, central_wl, bandwidth)

    for j, opd in enumerate(opd_values):
        # Calculate coherence degradation
        coherence_map[j, i] = coherence_degradation_by_cosine(fixed_bandwidth_wavelengths, weights, opd)

# Define actual OPD and center wavelength values for cross-sections
actual_opds = [1, 10, 50]  # Example OPD values (in microns)
actual_wavelengths = [230, 400, 800]  # Example center wavelengths (in nm)

# Create the figure with the desired layout
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1], wspace=0.3)

# Cross-section along the x-axis (center wavelength)
ax1 = fig.add_subplot(gs[0, 0])
for opd_value in actual_opds:
    opd_index = np.abs(opd_values - opd_value).argmin()  # Find the index of the actual OPD value
    ax1.plot(center_wavelengths, coherence_map[opd_index, :], label=f"OPD = {opd_value} μm")
ax1.set_xlabel("Center Wavelength (nm)")
ax1.set_ylabel("Coherence Parameter")
ax1.set_title("Cross-Section Along X-Axis")
ax1.legend(title="Optical Path Difference")
ax1.grid()

# Cross-section along the y-axis (OPD)
ax2 = fig.add_subplot(gs[1, 0])
for wl in actual_wavelengths:
    wl_index = np.abs(center_wavelengths - wl).argmin()  # Find the index of the actual wavelength value
    ax2.plot(opd_values, coherence_map[:, wl_index], label=f"Center Wavelength = {wl} nm")
ax2.set_xlabel("Optical Path Difference (μm)")
ax2.set_ylabel("Coherence Parameter")
ax2.set_title("Cross-Section Along Y-Axis")
ax2.legend(title="Center Wavelength")
ax2.grid()

# 2D map of coherence degradation
ax3 = fig.add_subplot(gs[:, 1])
extent = [
    center_wavelengths[0],
    center_wavelengths[-1],
    opd_values[0],  # OPD values in microns for y-axis
    opd_values[-1],  # OPD values in microns for y-axis
]
im = ax3.imshow(coherence_map, aspect="auto", extent=extent, origin="lower", cmap="viridis")
ax3.set_xlabel("Center Wavelength (nm)")
ax3.set_ylabel("Optical Path Difference (μm)")
ax3.set_title("Coherence Parameter Degradation")
cbar = fig.colorbar(im, ax=ax3, label="Coherence Parameter", fraction=0.046, pad=0.04)

# Adjust layout manually
fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1)

# Show the plot
plt.show()