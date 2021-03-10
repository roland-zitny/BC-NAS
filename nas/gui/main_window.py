from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget
from nas.gui.reg_window import RegWindow
from nas.src.user import User

qt_main_window_file = "gui/designs/main_window.ui"                   # .ui file.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qt_main_window_file)     # Load .ui file.


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
        Class used to display and manipulate with main window of graphic user interface.

        Methods
        --------
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
        """INFO"""

        if self.LoginLine.text():
            self.LoginErrorLabel.hide()
        else:
            self.LoginErrorLabel.show()

    def register(self):
        """
            Creates new user with his registration name and surname and creates
            new window for gathering user photo.
        """

        if self.RegUserName.text() and self.RegUserSurname.text():
            self.RegErrorLabel.hide()
            new_user = User(self.RegUserName.text(), self.RegUserSurname.text())
            self.reg_window = RegWindow(new_user)
            self.reg_window.show()
            self.hide()
        else:
            self.RegErrorLabel.show()
