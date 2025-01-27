import numpy as np
import matplotlib.pyplot as plt
from numpy.ma.core import argmax
from scipy.interpolate import interp1d

# Function to calculate intensity-based coherence degradation due to numerical aperture
def coherence_na_wl(center_wavelength, na, delta_z, num_rays, wavelengths, wl_weights):
    # Generate normalized radial distances within the NA
    r_values = np.linspace(0, 1, num_rays)  # Radial distances normalized to NA
    # na_weights = np.array([2 * np.pi * r * obs_profile(r * na) ** 2 for r in r_values]) # OBS usage
    na_weights = 2 * np.pi * r_values * obs_profile(r_values * na) ** 2
    # na_weights = 2 * np.pi * r_values # Simple flat top NA

    # Optical path difference (OPD) for each ray
    opd_rays = delta_z * 1000 * np.sqrt(1 + (r_values * na) ** 2)  # OPD for defocus

    # Phase shift for each ray
    phase_shifts = 2 * np.pi * opd_rays[:, np.newaxis] / wavelengths

    rows, cols = phase_shifts.shape
    middle_row = rows // 2
    middle_col = cols // 2

    # Incoherent intensity summation
    weights_map = na_weights[:, np.newaxis] * wl_weights
    intensities = weights_map * np.cos(phase_shifts - phase_shifts[0, middle_col])
    normalized_intensity = np.sum(intensities) / np.sum(na_weights)  # Normalize by total weight

    return normalized_intensity

# Gaussian weighting function
def gaussian_weights(wavelengths, center_wavelength, bandwidth):
    sigma = bandwidth / (2 * np.sqrt(2 * np.log(2)))  # Convert FWHM to standard deviation
    weights = np.exp(-((wavelengths - center_wavelength) ** 2) / (2 * sigma ** 2))
    return weights / np.sum(weights)  # Normalize the weights

def obs_profile(requested_na):
    OBS_intensity = [1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.9997, 0.9978, 0.9926, 0.9843, 0.9739, 0.9595, 0.9426, 0.9202, 0.8945, 0.8653, 0.8330, 0.7989, 0.7634, 0.7266, 0.6882, 0.6486, 0.6079, 0.5650, 0.5213, 0.4763, 0.4311, 0.3840, 0.3367, 0.2902, 0.2476, 0.2091, 0.1746, 0.1430, 0.1152, 0.0911, 0.0698, 0.0502, 0.0342, 0.0233, 0.0164, 0.0118, 0.0081, 0.0051, 0.0030, 0.0018, 0.0010, 0.0006, 0.0003, 0.0002, 0.0001, 0.0001, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]
    NA_vec = [0.0000, 0.0012, 0.0023, 0.0035, 0.0047, 0.0058, 0.0070, 0.0082, 0.0094, 0.0105, 0.0117, 0.0129, 0.0140, 0.0152, 0.0164, 0.0175, 0.0187, 0.0199, 0.0211, 0.0222, 0.0234, 0.0246, 0.0257, 0.0269, 0.0281, 0.0292, 0.0304, 0.0316, 0.0327, 0.0339, 0.0351, 0.0363, 0.0374, 0.0386, 0.0398, 0.0409, 0.0421, 0.0433, 0.0444, 0.0456, 0.0468, 0.0480, 0.0491, 0.0503, 0.0515, 0.0526, 0.0538, 0.0550, 0.0561, 0.0573, 0.0585, 0.0596, 0.0608, 0.0620, 0.0632, 0.0643, 0.0655, 0.0667, 0.0678, 0.0690, 0.0702, 0.0713, 0.0725, 0.0737, 0.0749, 0.0760, 0.0772, 0.0784, 0.0795, 0.0807, 0.0819, 0.0830, 0.0842, 0.0854, 0.0865, 0.0877, 0.0889, 0.0901, 0.0912, 0.0924, 0.0936, 0.0947, 0.0959, 0.0971, 0.0982, 0.0994, 0.1006, 0.1018, 0.1029, 0.1041, 0.1053, 0.1064, 0.1076, 0.1088, 0.1099, 0.1111, 0.1123, 0.1135, 0.1146, 0.1158, 0.1170, 0.1181, 0.1193, 0.1205, 0.1216, 0.1228, 0.1240, 0.1251, 0.1263]
    interp_func = interp1d(NA_vec, OBS_intensity, kind='linear')  # Linear interpolation
    return interp_func(requested_na)

# Parameters
center_wavelengths = np.linspace(200, 1000, 100)  # Center wavelengths (200 nm to 1000 nm)
bandwidth = 4  # Fixed bandwidth (2 nm)
delta_z_values = np.linspace(0, 100, 100)  # Focus shift (0 to 5 microns)
num_wavelengths = 100 # Number of wavelength samples
na = 0.12  # Numerical aperture using PRISM2 OBS
num_na_rays = 20  # Number of rays sampled

# Create a 2D grid for coherence degradation
coherence_map = np.zeros((len(delta_z_values), len(center_wavelengths)))

# Calculate coherence degradation for each center wavelength and focus shift
for i, central_wl in enumerate(center_wavelengths):
    # Generate wavelengths within the fixed bandwidth
    bandwidth_wavelengths = np.linspace(central_wl - 2 * bandwidth, central_wl + 2 * bandwidth, num_wavelengths)
    # Gaussian weights for the current center wavelength
    weights = gaussian_weights(bandwidth_wavelengths, central_wl, bandwidth)
    for j, delta_z in enumerate(delta_z_values):
        coherence_map[j, i] = np.abs(coherence_na_wl(central_wl, na, delta_z, num_na_rays, bandwidth_wavelengths, weights))


# Define actual focus shift and center wavelength values for cross-sections
actual_focus_shifts = [1, 10, 50]  # Example focus shifts (in microns)
# actual_wavelengths = [230, 400, 800]  # Example center wavelengths (in nm)
actual_wavelengths = [316, 480, 640]  # Example center wavelengths (in nm)

# Find the indices corresponding to the actual focus shifts and center wavelengths
focus_indices = [np.abs(delta_z_values - shift).argmin() for shift in actual_focus_shifts]
wl_indices = [np.abs(center_wavelengths - wl).argmin() for wl in actual_wavelengths]

# Plotting the OBS transmission curve
r_values = np.linspace(0, 1, 100)  # Radial distances normalized to NA
na_weights = r_values * obs_profile(r_values * na) ** 2
plt.plot(r_values*na, na_weights)

# Create the figure with the desired layout
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1], wspace=0.3)

# Cross-section along the x-axis (center wavelength)
ax1 = fig.add_subplot(gs[0, 0])
for focus_shift in actual_focus_shifts:
    focus_index = np.abs(delta_z_values - focus_shift).argmin()  # Find the index of the actual focus shift
    ax1.plot(center_wavelengths, coherence_map[focus_index, :], label=f"Focus Shift = {focus_shift:.2f} μm")
ax1.set_xlabel("Center Wavelength (nm)")
ax1.set_ylabel("Coherence")
ax1.set_title("Cross-Section Along X-Axis")
ax1.legend(title="Focus Shift")
ax1.grid()

# Cross-section along the y-axis (focus shift)
ax2 = fig.add_subplot(gs[1, 0])
for wl in actual_wavelengths:
    wl_index = np.abs(center_wavelengths - wl).argmin()  # Find the index of the actual wavelength value
    ax2.plot(delta_z_values, coherence_map[:, wl_index], label=f"Center Wavelength = {wl:.2f} nm")
ax2.set_xlabel("Focus Shift (μm)")
ax2.set_ylabel("Coherence")
ax2.set_title("Cross-Section Along Y-Axis")
ax2.legend(title="Center Wavelength")
ax2.grid()

# 2D map of coherence degradation
ax3 = fig.add_subplot(gs[:, 1])
extent = [
    center_wavelengths[0],
    center_wavelengths[-1],
    delta_z_values[0],  # Focus shift in microns for y-axis
    delta_z_values[-1],  # Focus shift in microns for y-axis
]
im = ax3.imshow(coherence_map, aspect="auto", extent=extent, origin="lower", cmap="viridis")
ax3.set_xlabel("Center Wavelength (nm)")
ax3.set_ylabel("Focus Shift (μm)")
ax3.set_title("Coherence degradation due to NA & WL SMearing")
cbar = fig.colorbar(im, ax=ax3, label="Coherence", fraction=0.046, pad=0.04)

# Adjust layout manually
fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1)

# Show the plot
plt.show()
