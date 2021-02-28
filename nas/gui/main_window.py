from PyQt5 import QtWidgets, uic
#from src.User import User
#from src.gui.RegistrationWindow import RegWindow

qtcreator_mainwindow_file = "gui/qtdesigns/main_window.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_mainwindow_file)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Addons to GUI

        # RegistrationWindow
        self.RegBtn.clicked.connect(self.ShowRegWindow)

    def ShowRegWindow(self):
        #self.reg_window = RegWindow()
        #self.reg_window.show()
        #self.hide()
        pass

    def create_new_user(self):
        name = self.RegUserName.text()
        surname = self.RegUserSurname.text()
        #new_user = User(name, surname)