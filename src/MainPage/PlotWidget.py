from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

import pyqtgraph as pg

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def addPointOnPlot(self, point: int):
        self.diametr.append(point)
        if len(self.diametr) > 10: self.diametr.pop(0)
        self.data_line.setData(self.time, self.diametr)
        

    def initUI(self):
        the_graph_of_diameter_changes = pg.PlotWidget()
        the_graph_of_diameter_changes.setBackground("w")
        
        pen = pg.mkPen(color=(255, 0, 0))
        self.time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.diametr = []
        self.data_line = the_graph_of_diameter_changes.plot(self.time, self.diametr, pen=pen)
        h_box_layout_graph_widget = QHBoxLayout()
        h_box_layout_graph_widget.addWidget(the_graph_of_diameter_changes, 1)
        
        self.setLayout(h_box_layout_graph_widget)