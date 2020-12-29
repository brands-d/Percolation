import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from ..plot.plot import Plot
#from percolation.model.model import PercolationModel

UI, _ = uic.loadUiType(os.path.splitext(__file__)[0] + '.ui')


class MainWindow(QMainWindow, UI):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.setup()
        self.connect()

    def setup(self):
        pass

    def connect(self):
        pass
