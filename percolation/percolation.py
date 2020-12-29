import qdarkstyle

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from percolation.gui.mainwindow.mainwindow import MainWindow
from percolation import __version__, __project__, __directory__


class Percolation(QApplication):

    def __init__(self, *args):
        super().__init__(*args)
        self.setApplicationVersion(__version__)
        self.setApplicationName(__project__)
        self.setDesktopFileName(__project__)
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.setWindowIcon(
            QIcon(str(__directory__ / 'resources/images/icon.png')))

    def run(self):
        main_window = MainWindow()
        main_window.show()

        return super().exec_()
