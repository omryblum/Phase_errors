import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# import mainDialog as mainDialog
import sys

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random

# Handle high resolution displays:
if hasattr(PyQt5.QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(PyQt5.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_UseHighDpiPixmaps, True)

# class MainDialog(QDialog, mainDialog.Ui_Dialog):
class MainDialog(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self)
        loadUi("MainWindow.ui", self)

        self.pushButton.clicked.connect(self.push_button_clicked)
        self.lineEdit.returnPressed.connect(self.line_edit_pressed)

        self.setWindowTitle("Matplotlib Example GUI")
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))

    def push_button_clicked(self):
        self.textBrowser.setText(f'the checkbox is marked {str(self.checkBox.isChecked())}, '
                                 f'and included string {self.lineEdit.text()}')

        fs = 500
        f = random.randint(1, 100)
        ts = 1 / fs
        length_of_signal = 100
        t = np.linspace(0, 1, length_of_signal)
        cosinus_signal = np.cos(2 * np.pi * f * t)
        sinus_signal = np.sin(2 * np.pi * f * t)
        self.MplWidget.canvas.axes.clear()
        self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        self.MplWidget.canvas.axes.plot(t, sinus_signal)
        self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        self.MplWidget.canvas.draw()

    def line_edit_pressed(self):
        if self.lineEdit.text().isnumeric():
            self.progressBar.setValue(int(self.lineEdit.text()))

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