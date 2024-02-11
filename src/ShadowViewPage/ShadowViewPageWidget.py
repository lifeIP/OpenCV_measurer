from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class ShadowViewPageWidget(QWidget):
    def __init__(self, width:int, height:int):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()

    @pyqtSlot(QImage)
    def setImage0(self, image):
        self.label_shadow_0.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setImage1(self, image):
        self.label_shadow_1.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(int)
    def setDelata_x(self, width):
        self.label_shadow_0_delta_x.setText("ΔX: " + str(width))
    
    @pyqtSlot(int)
    def setDelata_y(self, width):
        self.label_shadow_1_delta_y.setText("ΔY: " + str(width))

    def initUI(self):
        # Первая вкладка +++++++++++++++++++++++++++++++++++++++++++++++++++
        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_0 = QLabel()
        self.label_shadow_0.setMinimumSize(int(self.width * 0.9), int(self.height * 0.2))

        self.label_shadow_0_delta_x = QLabel()
        self.label_shadow_0_delta_x.setText("ΔX: ")
        self.label_shadow_0_delta_x.setMinimumSize(int(self.width * 0.1), int(self.height * 0.2))

        
        self.h_box_layout_0 = QHBoxLayout()
        self.h_box_layout_0.addWidget(self.label_shadow_0)
        self.h_box_layout_0.addWidget(self.label_shadow_0_delta_x)
        # Первая картинка --------------------------------------------------
        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_1 = QLabel()
        self.label_shadow_1.setMinimumSize(int(self.width * 0.9), int(self.height * 0.2))

        self.label_shadow_1_delta_y = QLabel()
        self.label_shadow_1_delta_y.setText("ΔY: ")
        self.label_shadow_1_delta_y.setMinimumSize(int(self.width * 0.1), int(self.height * 0.2))

        self.h_box_layout_1 = QHBoxLayout()
        self.h_box_layout_1.addWidget(self.label_shadow_1)
        self.h_box_layout_1.addWidget(self.label_shadow_1_delta_y)
        # Вторая картинка --------------------------------------------------
        # Первая вкладка ---------------------------------------------------

        self.v_box_layout_0 = QVBoxLayout()
        self.v_box_layout_0.addLayout(self.h_box_layout_0)
        self.v_box_layout_0.addLayout(self.h_box_layout_1)
        
        self.setLayout(self.v_box_layout_0)
