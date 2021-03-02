from PyQt5 import QtWidgets, uic

qt_stimuli_presentation_file = "gui/designs/stimuli_presentation.ui"                    # .ui file.
Ui_RegWindow, QtBaseClass = uic.loadUiType(qt_stimuli_presentation_file)


class StimuliPresentation(QtWidgets.QMainWindow, Ui_RegWindow):
    def __init__(self, reg_user):
        QtWidgets.QMainWindow.__init__(self)
        Ui_RegWindow.__init__(self)
        self.setupUi(self)
