import os
import pickle
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from nas.gui.registration_window import RegistrationWindow
from nas.gui.login_stimulation_window import LoginStimulationPresentation
from nas.src.user import User
import nas.src.config as config

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "main_window.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_path)  # Load .ui file.


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
        Class for displaying the main window of the graphical user interface and its manipulation.
        The user can register or log in.
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
            Makes other window settings, such as connecting buttons, etc.
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
        self.LoginBtn.clicked.connect(self.log_in)

    def log_in(self):
        """
            Checks whether the user is registered and if so, continues by opening the ``login_stimulation_window``.
            The ``user`` object created during registration is loaded.
        """

        if self.LoginLine.text():
            self.LoginErrorLabel.hide()
            if not self.check_id(self.LoginLine.text()):
                self.LoginErrorLabel.setText("Užívateľ nie je registrovaný")
                self.LoginErrorLabel.show()
            else:
                pickle_path = os.path.join(config.DB_DIR + os.sep + self.LoginLine.text() + ".p")
                pickle_file = open(pickle_path, 'rb')
                user = pickle.load(pickle_file)
                pickle_file.close()

                self.login_window = LoginStimulationPresentation(user)
                self.login_window.showMaximized()
                self.hide()

        else:
            self.LoginErrorLabel.setText("Formulár musí byť vyplnený")
            self.LoginErrorLabel.show()

    def register(self):
        """
            Checks if the user is registered and if not, continues by opening ``reg_window``.
            Creates new ``user`` with his `name`, `surname` and `login ID`.
        """

        if self.RegUserName.text() and self.RegUserSurname.text() and self.RegUserLogin.text():
            self.RegErrorLabel.hide()
            # Check if login is available.
            if not self.check_id(self.RegUserLogin.text()):
                # Creates user object with name, surname and login name.
                new_user = User(self.RegUserName.text(), self.RegUserSurname.text(), self.RegUserLogin.text())
                self.reg_window = RegistrationWindow(new_user)
                self.reg_window.showMaximized()
                self.hide()
            else:
                self.RegErrorLabel.setText("Prihlasovacie meno už existuje")
                self.RegErrorLabel.show()
        else:
            self.RegErrorLabel.setText("Formulár musí byť vyplnený")
            self.RegErrorLabel.show()

    @staticmethod
    def check_id(login):
        """
            Check if user login exists in database.

            :param login: User login ID.
            :type login: string

            :return: True if login exists in database, false if login is available.
            :rtype: bool
        """

        if os.path.exists(os.path.join(config.DB_DIR + os.sep + login + ".p")):
            return True
        else:
            return False
