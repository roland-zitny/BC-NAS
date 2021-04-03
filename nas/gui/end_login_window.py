import base64
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtMultimedia
from PyQt5 import QtMultimediaWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDesktopWidget
import config

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "end_login_window.ui")
Ui_RegWindow, QtBaseClass = uic.loadUiType(ui_path)  # Load .ui file.


class EndLoginWindow(QtWidgets.QMainWindow, Ui_RegWindow):
    def __init__(self, reg_user, system_access):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        self.reg_user = reg_user
        self.system_access = system_access

        self.set_up_window()

    def set_up_window(self):
        """
            Makes other window settings, such as connecting buttons, etc.
        """

        # Center window to screen.
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        if self.system_access == 1:
            self.EndInfo.setText(self.EndInfo.text() + " ÚSPEŠNÉ")
        else:
            self.EndInfo.setText(self.EndInfo.text() + " NEÚSPEŠNÉ")
