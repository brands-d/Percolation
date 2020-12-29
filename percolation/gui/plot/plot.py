from pyqtgraph import ImageView, PlotItem

from PyQt5.QtWidgets import QSizePolicy


class Plot(ImageView):

    def __init__(self, *args, **kwargs):
        self.plot_view = PlotItem(lockAspect=1)
        super(Plot, self).__init__(*args, view=self.plot_view, **kwargs)

        self.setup()
        self.show()

    def plot(self, grid):
        self.clear()

        self.setImage(grid.config)

    def setup(self):
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.view.invertY(True)
        self.view.hideButtons()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()
