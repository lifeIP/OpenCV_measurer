from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class OriginalViewPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage, QImage)
    def setImages(self, image: QImage, image2: QImage):
        self.label_shadow_2.setPixmap(QPixmap.fromImage(image))
        self.label_shadow_3.setPixmap(QPixmap.fromImage(image2))

    def initUI(self):
        # Вторая вкладка +++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_2 = QLabel()
        self.label_shadow_2.setMinimumSize(int(self.width() * 0.95), int(self.height() * 0.5))
        self.label_shadow_2.setScaledContents(True)
        
        self.label_shadow_3 = QLabel()
        self.label_shadow_3.setMinimumSize(int(self.width() * 0.95), int(self.height() * 0.5))
        self.label_shadow_3.setScaledContents(True)
        # Вторая вкладка ---------------------------------------------------
        self.v_box_layout_tab_1 = QVBoxLayout()
        self.v_box_layout_tab_1.addWidget(self.label_shadow_2)
        self.v_box_layout_tab_1.addWidget(self.label_shadow_3)
        self.setLayout(self.v_box_layout_tab_1)
