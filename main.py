import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import mainDialog as mainDialog

import sys
import requests

# Handle high resolution displays:
if hasattr(PyQt5.QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(PyQt5.QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(PyQt5.QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MainDialog(QDialog, mainDialog.Ui_Dialog):

    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.push_button_clicked)
        self.lineEdit.returnPressed.connect(self.line_edit_pressed)

    def push_button_clicked(self):
        self.textBrowser.setText(f'the checkbox is marked {str(self.checkBox.isChecked())}, '
                                 f'and included string {self.lineEdit.text()}')

    def line_edit_pressed(self):
        if self.lineEdit.text().isnumeric():
            self.progressBar.setValue(int(self.lineEdit.text()))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = MainDialog()
    form.show()
    app.exec_()