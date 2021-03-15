import os
from os import path
import pickle
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from nas.gui.reg_window import RegWindow
from nas.gui.login_stim_window import LoginStimuliPresentation
from nas.src.user import User
from nas.src import config

qt_main_window_file = "gui/designs/main_window.ui"  # .ui file.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_main_window_file)  # Load .ui file.


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
        Class used to display and manipulate with main window of graphic user interface.

        Methods
        --------
        set_up_window()
            Set up all necessary parameters of window.

        register()
            Registration process.

        login()
            Login process.
    """

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.reg_window = None
        self.login_window = None
        self.set_up_window()

    def set_up_window(self):
        """
            Set up additional parameters of window.
        """

        # Hide widgets.
        self.LoginErrorLabel.hide()
        self.RegErrorLabel.hide()

        # Center window to screen.
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Connect ui buttons to methods.
        self.RegistrationBtn.clicked.connect(self.register)
        self.LoginBtn.clicked.connect(self.login)

    def login(self):
        """
            If user is registered load his data and continue login.
        """

        if self.LoginLine.text():
            self.LoginErrorLabel.hide()
            if self.check_login_possibility(self.LoginLine.text()):
                self.LoginErrorLabel.setText("Užívateľ nie je registrovaný")
                self.LoginErrorLabel.show()
            else:
                pickle_path = os.path.join(config.DB_DIR + os.sep + self.LoginLine.text() + ".p")
                pickle_file = open(pickle_path, 'rb')
                user = pickle.load(pickle_file)
                pickle_file.close()

                self.login_window = LoginStimuliPresentation(user)
                self.login_window.showMaximized()
                self.hide()

        else:
            self.LoginErrorLabel.setText("Formulár musí byť vyplnený")
            self.LoginErrorLabel.show()

    def register(self):
        """
            Creates new user with his registration name, surname and user login name.
            Creates new window for gathering user photo.
        """

        if self.RegUserName.text() and self.RegUserSurname.text() and self.RegUserLogin.text():
            self.RegErrorLabel.hide()
            # Check if login is available.
            if self.check_login_possibility(self.RegUserLogin.text()):
                # Creates user object with name, surname and login name.
                new_user = User(self.RegUserName.text(), self.RegUserSurname.text(), self.RegUserLogin.text())
                self.reg_window = RegWindow(new_user)
                self.reg_window.showMaximized()
                self.hide()
            else:
                self.RegErrorLabel.setText("Prihlasovacie meno už existuje")
                self.RegErrorLabel.show()
        else:
            self.RegErrorLabel.setText("Formulár musí byť vyplnený")
            self.RegErrorLabel.show()

    def check_login_possibility(self, login) -> bool:
        """
            Check is user login is available.

            Attributes
            ----------
                login: login name

            Return
            ------
                True -> not available
                False -> available
        """

        if path.exists(os.path.join(config.DB_DIR + os.sep + login + ".p")):
            return False
        else:
            return True
