from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class ShadowViewPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage, QImage)
    def setImages(self, image: QImage, image2: QImage):
        self.label_shadow_0.setPixmap(QPixmap.fromImage(image))
        self.label_shadow_1.setPixmap(QPixmap.fromImage(image2))

    @pyqtSlot(int, int)
    def setDelata_x_and_y(self, width_x: int, width_y: int):
        self.label_shadow_0_delta_x.setText("ΔX: " + str(width_x))
        self.label_shadow_1_delta_y.setText("ΔY: " + str(width_y))

    def initUI(self):
        # Первая вкладка +++++++++++++++++++++++++++++++++++++++++++++++++++
        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_0 = QLabel()
        self.label_shadow_0.setMinimumSize(int(self.width() * 0.9), int(self.height() * 0.2))
        self.label_shadow_0.setScaledContents(True)

        self.label_shadow_0_delta_x = QLabel()
        self.label_shadow_0_delta_x.setText("ΔX: ")
        self.label_shadow_0_delta_x.setMinimumSize(int(self.width() * 0.1), int(self.height() * 0.2))
        
        self.h_box_layout_0 = QHBoxLayout()
        self.h_box_layout_0.addWidget(self.label_shadow_0, 9)
        self.h_box_layout_0.addWidget(self.label_shadow_0_delta_x, 1)
        # Первая картинка --------------------------------------------------
        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_1 = QLabel()
        self.label_shadow_1.setMinimumSize(int(self.width() * 0.9), int(self.height() * 0.2))
        self.label_shadow_1.setScaledContents(True)

        self.label_shadow_1_delta_y = QLabel()
        self.label_shadow_1_delta_y.setText("ΔY: ")
        self.label_shadow_1_delta_y.setMinimumSize(int(self.width() * 0.1), int(self.height() * 0.2))

        self.h_box_layout_1 = QHBoxLayout()
        self.h_box_layout_1.addWidget(self.label_shadow_1, 9)
        self.h_box_layout_1.addWidget(self.label_shadow_1_delta_y, 1)
        # Вторая картинка --------------------------------------------------
        # Первая вкладка ---------------------------------------------------

        self.v_box_layout_0 = QVBoxLayout()
        self.v_box_layout_0.addLayout(self.h_box_layout_0, 1)
        self.v_box_layout_0.addLayout(self.h_box_layout_1, 1)
        
        self.setLayout(self.v_box_layout_0)
