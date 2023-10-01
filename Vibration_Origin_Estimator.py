import PyQt5
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np


# Handle high resolution displays:
# if hasattr(PyQt5.QtCore.Qt, 'AA_EnableHighDpiScaling'):
#     PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling, True)
# if hasattr(PyQt5.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
#     PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_UseHighDpiPixmaps, True)

# class MainDialog(QDialog, mainDialog.Ui_Dialog):
class MainDialog(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        loadUi("Vibration_Origin_Estimator.ui", self)

        self.pushButton.clicked.connect(self.push_button_clicked)

        # self.setWindowTitle("Vibration Origin Estimator")
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    ### UI Functions ###
    def push_button_clicked(self):
        known_peaks = {}
        for ind in range(self.tableWidget.rowCount()):
            fps, freq = self.tableWidget.item(ind, 0), self.tableWidget.item(ind, 1)
            if fps is not None and freq is not None:
                known_peaks[int(fps.text())] = int(freq.text())

        # known_peaks format is: FPS -> frequency
        frequencies = np.arange(1, 600)
        merit = np.zeros(frequencies.size)

        for ind, freq in enumerate(frequencies):
            mapping = self.peak_mapping_for_tested_frequency(freq, known_peaks.copy())
            for fps in mapping:
                # merit[ind] += np.abs(mapping[fps] - known_peaks[fps])
                merit[ind] += (mapping[fps] - known_peaks[fps]) ** 2

        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(frequencies, 100 / (merit + 1), linewidth=2)
        self.MplWidget.canvas.axes.set_title(f'Most probable origin frequency is {frequencies[np.argmin(merit)]:.0f} Hz')
        self.MplWidget.canvas.axes.set_xlabel('Frequency'), self.MplWidget.canvas.axes.set_ylabel('Score')
        self.MplWidget.canvas.figure._tight = True
        self.MplWidget.canvas.axes.grid()
        self.MplWidget.canvas.draw()


    ### Calculation fucntions ###
    def peak_mapping_for_tested_frequency(self, freq, fps):
        mapping = fps
        for f in fps:
            peaks = np.unique(np.concatenate((freq + np.arange(-10, 10) * f, np.arange(-10, 10) * f - freq)))
            single_peak = peaks[np.logical_and(peaks >= 0, peaks < f / 2)]
            assert (single_peak.size == 1)
            mapping[f] = int(single_peak)

        return mapping


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    app.exec_()

#     def update_graph(self):
#         fs = 500
#         f = random.randint(1, 100)
#         ts = 1 / fs
#         length_of_signal = 100
#         t = np.linspace(0, 1, length_of_signal)
#
#         cosinus_signal = np.cos(2 * np.pi * f * t)
#         sinus_signal = np.sin(2 * np.pi * f * t)
#
#         self.MplWidget.canvas.axes.clear()
#         self.MplWidget.canvas.axes.plot(t, cosinus_signal)
#         self.MplWidget.canvas.axes.plot(t, sinus_signal)
#         self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
#         self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
#         self.MplWidget.canvas.draw()
#
#
