import os
from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget

directory_path = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(directory_path, "designs" + os.sep + "end_identification_window.ui")
Ui_RegWindow, QtBaseClass = uic.loadUiType(ui_path)  # Load .ui file.


class EndIdWindow(QtWidgets.QMainWindow, Ui_RegWindow):
    """
        Class to display the success of a user login.

        :param reg_user: The object of the registered user.
        :type reg_user: ``user``
        :param user_id: user_id.
        :type system_access: bool
    """

    def __init__(self, user_id):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
        self.user_id = user_id

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

        if self.user_id is not None:
            self.EndInfo.setText(self.EndInfo.text() + self.user_id)
        else:
            self.EndInfo.setText(self.EndInfo.text() + "Nemožno určiť")
