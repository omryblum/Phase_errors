import numpy as np
import matplotlib.pyplot as plt

def peak_mapping_for_tested_frequency(freq, fps):
    mapping = fps
    for f in fps:
        peaks = np.unique(np.concatenate((freq + np.arange(-10, 10) * f, np.arange(-10, 10) * f - freq)))
        single_peak = peaks[np.logical_and(peaks >= 0, peaks < f/2)]
        assert(single_peak.size == 1)
        mapping[f] = int(single_peak)

    return mapping


# Start by loading data from user
known_peaks = {221: 4, 215: 3, 209: 10}  # format is: FPS -> frequency
frequencies = np.arange(1, 600)
merit = np.zeros(frequencies.size)

for ind, freq in enumerate(frequencies):
    mapping = peak_mapping_for_tested_frequency(freq, known_peaks.copy())
    for fps in mapping:
        merit[ind] += (mapping[fps] - known_peaks[fps])**2

fig, ax = plt.subplots(1, 1)
# fig.dpi = 100
fig._tight = True

fig.axes[0].plot(frequencies, 100/(merit+1), linewidth=2)
fig.axes[0].title._text = f'Most probably origin frequency is {frequencies[np.argmin(merit)]:.0f} Hz'
fig.axes[0].xaxis.label._text, fig.axes[0].yaxis.label._text = 'Frequency', 'Score'

[ax.grid() for ax in fig.axes]
plt.get_current_fig_manager().window.showMaximized()
plt.show()