from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class SettingsPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    @pyqtSlot(QImage, QImage)
    def setImages(self, image: QImage, image2: QImage):
        self.label_setting_0.setPixmap(QPixmap.fromImage(image))
        self.label_setting_1.setPixmap(QPixmap.fromImage(image2))
    
    def initUI(self):
        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_0 = QLabel()
        self.label_setting_0.setMinimumSize(int(self.width() * 0.9), int(self.height() * 0.2))
        self.label_setting_0.setScaledContents(True)
        # Первая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_1 = QLabel()
        self.label_setting_1.setMinimumSize(int(self.width() * 0.9), int(self.height() * 0.2))
        self.label_setting_1.setScaledContents(True)
        # Вторая картинка --------------------------------------------------


        self.v_box_layout_setting_0 = QVBoxLayout()
        self.v_box_layout_setting_0.addWidget(self.label_setting_0, 1)
        self.v_box_layout_setting_0.addWidget(self.label_setting_1, 1)
        
        self.setLayout(self.v_box_layout_setting_0)