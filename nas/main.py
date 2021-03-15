import sys
from PyQt5 import QtWidgets
from nas.gui import main_window


def main():
    """Main program."""

    app = QtWidgets.QApplication(sys.argv)
    window = main_window.MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
