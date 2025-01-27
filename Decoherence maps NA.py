import numpy as np
import matplotlib.pyplot as plt

# Function to calculate intensity-based coherence degradation due to numerical aperture
def incoherent_coherence_due_to_na(center_wavelength, na, delta_z, num_rays=100):
    # Generate normalized radial distances within the NA
    r_values = np.linspace(0, 1, num_rays)  # Radial distances normalized to NA
    weights = 2 * np.pi * r_values  # Weighting for circular aperture

    # Optical path difference (OPD) for each ray
    # opd_rays = delta_z * (1 - np.sqrt(1 - r_values ** 2))  # OPD for defocus
    opd_rays = delta_z * 1000 * (1 - np.sqrt((1 - (r_values * na) ** 2)))  # OPD for defocus

    # Phase shift for each ray
    phase_shifts = 2 * np.pi * opd_rays / center_wavelength

    # Incoherent intensity summation
    intensities = weights * np.cos(phase_shifts)
    normalized_intensity = np.sum(intensities) / np.sum(weights)  # Normalize by total weight
    return normalized_intensity

# Parameters
center_wavelengths = np.linspace(200, 1000, 100)  # Center wavelengths (500 nm to 600 nm)
delta_z_values = np.linspace(0, 50, 100)  # Focus shift (0 to 5 microns)
na = 0.1  # Numerical aperture (example value)
num_rays = 100  # Number of rays sampled

# Create a 2D grid for coherence degradation
coherence_map_na = np.zeros((len(delta_z_values), len(center_wavelengths)))

# Calculate coherence degradation for each center wavelength and focus shift
for i, central_wl in enumerate(center_wavelengths):
    for j, delta_z in enumerate(delta_z_values):
        coherence_map_na[j, i] = incoherent_coherence_due_to_na(central_wl, na, delta_z, num_rays)

# Define actual focus shift and center wavelength values for cross-sections
actual_focus_shifts = [1, 10, 50]  # Example focus shifts (in microns)
actual_wavelengths = [230, 400, 800]  # Example center wavelengths (in nm)

# Find the indices corresponding to the actual focus shifts and center wavelengths
focus_indices = [np.abs(delta_z_values - shift).argmin() for shift in actual_focus_shifts]
wl_indices = [np.abs(center_wavelengths - wl).argmin() for wl in actual_wavelengths]

# Create the figure with the desired layout
fig = plt.figure(figsize=(15, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[1, 2], height_ratios=[1, 1], wspace=0.3)

# Cross-section along the x-axis (center wavelength)
ax1 = fig.add_subplot(gs[0, 0])
for focus_shift in actual_focus_shifts:
    focus_index = np.abs(delta_z_values - focus_shift).argmin()  # Find the index of the actual focus shift
    ax1.plot(center_wavelengths, coherence_map_na[focus_index, :], label=f"Focus Shift = {focus_shift:.2f} μm")
ax1.set_xlabel("Center Wavelength (nm)")
ax1.set_ylabel("Coherence Parameter")
ax1.set_title("Cross-Section Along X-Axis")
ax1.legend(title="Focus Shift")
ax1.grid()

# Cross-section along the y-axis (focus shift)
ax2 = fig.add_subplot(gs[1, 0])
for wl in actual_wavelengths:
    wl_index = np.abs(center_wavelengths - wl).argmin()  # Find the index of the actual wavelength value
    ax2.plot(delta_z_values, coherence_map_na[:, wl_index], label=f"Center Wavelength = {wl:.2f} nm")
ax2.set_xlabel("Focus Shift (μm)")
ax2.set_ylabel("Coherence Parameter")
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
im = ax3.imshow(coherence_map_na, aspect="auto", extent=extent, origin="lower", cmap="viridis")
ax3.set_xlabel("Center Wavelength (nm)")
ax3.set_ylabel("Focus Shift (μm)")
ax3.set_title("Coherence Parameter Degradation Due to NA")
cbar = fig.colorbar(im, ax=ax3, label="Coherence Parameter", fraction=0.046, pad=0.04)

# Adjust layout manually
fig.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.1)

# Show the plot
plt.show()
