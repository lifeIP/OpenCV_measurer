from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

import pyqtgraph as pg

class MainPageWidget(QWidget):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()
    
    @pyqtSlot(float, float)
    def setDiametr_and_ovality(self, diametr: float, ovality: float):
        self.label_data_diametr_view.setText(diametr)

    @pyqtSlot(int, int)
    def setPointPosition(self, pos_x, pos_y):
        self

    def initUI(self):
        from src.MainPage.DrawCircle import DrawCircle
        circularWidget = DrawCircle()

        label_name_diametr = QLabel("ДИАМЕТР, пиксели")
        self.label_data_diametr_view = QLabel("Что-то не работает")
        
        v_box_layout_data_diametr_view = QVBoxLayout()
        v_box_layout_data_diametr_view.addWidget(label_name_diametr, 1)
        v_box_layout_data_diametr_view.addWidget(self.label_data_diametr_view, 1)
        data_diametr_view_frame = QFrame()
        data_diametr_view_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        data_diametr_view_frame.setLineWidth(1)
        data_diametr_view_frame.setLayout(v_box_layout_data_diametr_view)


        label_name_ovality = QLabel("ОВАЛЬНОСТЬ, пиксели")
        self.label_data_ovality_view = QLabel("Что-то не работает")

        v_box_layout_data_ovality_view = QVBoxLayout()
        v_box_layout_data_ovality_view.addWidget(label_name_ovality, 1)
        v_box_layout_data_ovality_view.addWidget(self.label_data_ovality_view, 1)
        data_ovality_view_frame = QFrame()
        data_ovality_view_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        data_ovality_view_frame.setLineWidth(1)
        data_ovality_view_frame.setLayout(v_box_layout_data_ovality_view)


        v_box_layout_common_data = QVBoxLayout()
        v_box_layout_common_data.addWidget(data_diametr_view_frame, 1)
        v_box_layout_common_data.addWidget(data_ovality_view_frame, 1)

        h_box_layout_centering_widget = QHBoxLayout()
        h_box_layout_centering_widget.addWidget(circularWidget, 5)
        h_box_layout_centering_widget.addLayout(v_box_layout_common_data, 2)


        
        the_graph_of_diameter_changes = pg.PlotWidget()
        the_graph_of_diameter_changes.setBackground("w")
        pen = pg.mkPen(color=(255, 0, 0))
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        diametr = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        the_graph_of_diameter_changes.plot(time, diametr, pen=pen)
        h_box_layout_graph_widget = QHBoxLayout()
        h_box_layout_graph_widget.addWidget(the_graph_of_diameter_changes, 1)


        graph_frame = QFrame()
        graph_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        graph_frame.setLineWidth(1)
        graph_frame.setLayout(h_box_layout_graph_widget)

        v_box_layout_central_and_gtaph = QVBoxLayout()
        v_box_layout_central_and_gtaph.addLayout(h_box_layout_centering_widget, 3)
        v_box_layout_central_and_gtaph.addWidget(graph_frame, 2)

        self.setLayout(v_box_layout_central_and_gtaph)
