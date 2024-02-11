from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class OriginalViewPageWidget(QWidget):
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage)
    def setImage2(self, image):
        self.label_shadow_2.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setImage3(self, image):
        self.label_shadow_3.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        # Вторая вкладка +++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_2 = QLabel()
        self.label_shadow_2.setMinimumSize(int(self.width * 0.95), int(self.height * 0.5))
        self.label_shadow_3 = QLabel()
        self.label_shadow_3.setMinimumSize(int(self.width * 0.95), int(self.height * 0.5))
        # Вторая вкладка ---------------------------------------------------
        self.v_box_layout_tab_1 = QVBoxLayout()
        self.v_box_layout_tab_1.addWidget(self.label_shadow_2)
        self.v_box_layout_tab_1.addWidget(self.label_shadow_3)
        self.setLayout(self.v_box_layout_tab_1)
