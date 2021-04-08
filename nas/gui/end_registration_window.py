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
from nas.gui.login_stimulation_window import LoginStimulationPresentation
import config

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "end_registration_window.ui")
Ui_RegWindow, QtBaseClass = uic.loadUiType(ui_path)  # Load .ui file.


class EndRegistrationWindow(QtWidgets.QMainWindow, Ui_RegWindow):
    """
        Class to display the final window that confirms the registration.
        The user can perform a test login from this window.

        :param reg_user: The object of the registered user.
        :type reg_user: ``user``
    """

    def __init__(self, reg_user):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        self.reg_user = reg_user

        self.login_window = None

        self.set_up_window()
        self.get_reaction_plot()
        self.set_end_figure()

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

        self.end_name.setText(self.end_name.text() + "  " + self.reg_user.get_name())
        self.end_surname.setText(self.end_surname.text() + "  " + self.reg_user.get_surname())
        self.end_loginId.setText(self.end_loginId.text() + "  " + self.reg_user.get_id())

        self.TestLogin.clicked.connect(self.testing_log_in)

    def get_reaction_plot(self):
        """
            Creates a graph of responses to self-face and non-self-face stimuli.
            This graph is stored at `TMP_END_FIGURE`.
        """

        reactions, react_types = self.reg_user.get_reg_data()

        self_face_reaction = None
        non_self_face_reaction = None

        for i in range(len(react_types)):
            if react_types[i] == 1:
                self_face_reaction = reactions[i]
                non_self_face_reaction = reactions[i + 1]
                break

        fig, axs = plt.subplots(2)
        fig.suptitle('Self-face & Non-self-face reakcia')
        axs[0].plot(self_face_reaction[3])
        axs[0].set_title('Self-face')
        axs[1].plot(non_self_face_reaction[3])
        axs[1].set_title('Non-self-face')
        plt.setp(axs[0], ylabel='mV')
        plt.setp(axs[1], ylabel='mV')
        fig.tight_layout()
        plt.savefig(config.TMP_END_FIGURE)

    def set_end_figure(self):
        """
            Draw a graph of the reaction in the window.
        """

        pixmap = QPixmap(config.TMP_END_FIGURE)
        self.ReactionLabel.setPixmap(QPixmap(pixmap.scaledToHeight(500)))
        self.clean_tmp()

    @staticmethod
    def clean_tmp():
        """
            Cleans up the temporary files folder.
        """

        os.remove(config.TMP_END_FIGURE)
        os.remove(config.TMP_PHOTO)
        os.remove(config.TMP_PROC_PHOTO)

    def testing_log_in(self):
        """
            Performs a test login.
        """

        self.login_window = LoginStimulationPresentation(self.reg_user)
        self.login_window.showMaximized()
        self.hide()
