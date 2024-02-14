from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

import pyqtgraph as pg

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        the_graph_of_diameter_changes = pg.PlotWidget()
        the_graph_of_diameter_changes.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        diametr = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        the_graph_of_diameter_changes.plot(time, diametr, pen=pen)
        h_box_layout_graph_widget = QHBoxLayout()
        h_box_layout_graph_widget.addWidget(the_graph_of_diameter_changes, 1)
        
        self.setLayout(h_box_layout_graph_widget)