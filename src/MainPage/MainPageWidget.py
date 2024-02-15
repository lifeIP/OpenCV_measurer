from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

import pyqtgraph as pg

class MainPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    @pyqtSlot(float, float)
    def setDiametr_and_ovality(self, diametr: float, ovality: float):
        self.label_data_diametr_view.setText(diametr)
        self.label_data_ovality_view.setText(ovality)

    @pyqtSlot(float, float)
    def setPointPosition(self, pos_x: float, pos_y: float):
        self.circularWidget.setPointPos(pos_x, pos_y)


    def initUI(self):
        from src.MainPage.DrawCircle import DrawCircle
        self.circularWidget = DrawCircle()

        label_name_diametr = QLabel("ДИАМЕТР, пиксели")
        label_name_diametr.setAlignment(Qt.AlignCenter)
        self.label_data_diametr_view = QLabel("Что-то не работает")
        self.label_data_diametr_view.setAlignment(Qt.AlignCenter)
        
        v_box_layout_data_diametr_view = QVBoxLayout()
        v_box_layout_data_diametr_view.addWidget(label_name_diametr, 1)
        v_box_layout_data_diametr_view.addWidget(self.label_data_diametr_view, 1)
        data_diametr_view_frame = QFrame()
        data_diametr_view_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        data_diametr_view_frame.setLineWidth(1)
        data_diametr_view_frame.setLayout(v_box_layout_data_diametr_view)


        label_name_ovality = QLabel("ОВАЛЬНОСТЬ, пиксели")
        label_name_ovality.setAlignment(Qt.AlignCenter)
        self.label_data_ovality_view = QLabel("Что-то не работает")
        self.label_data_ovality_view.setAlignment(Qt.AlignCenter)

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
        h_box_layout_centering_widget.addWidget(self.circularWidget, 5)
        h_box_layout_centering_widget.addLayout(v_box_layout_common_data, 2)

 
        from src.MainPage.PlotWidget import PlotWidget
        self.plotWidget = PlotWidget()
        h_box_layout_graph_widget = QHBoxLayout()
        h_box_layout_graph_widget.addWidget(self.plotWidget, 1)

        graph_frame = QFrame()
        graph_frame.setFrameStyle(QFrame.Panel | QFrame.Plain)
        graph_frame.setLineWidth(1)
        graph_frame.setLayout(h_box_layout_graph_widget)

        v_box_layout_central_and_gtaph = QVBoxLayout()
        v_box_layout_central_and_gtaph.addLayout(h_box_layout_centering_widget, 3)
        v_box_layout_central_and_gtaph.addWidget(graph_frame, 2)

        self.setLayout(v_box_layout_central_and_gtaph)
