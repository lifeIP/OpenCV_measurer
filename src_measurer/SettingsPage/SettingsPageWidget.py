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
    
    @pyqtSlot(QImage, QImage)
    def setImages1(self, image3: QImage, image4: QImage):
        self.label_setting_2.setPixmap(QPixmap.fromImage(image3))
        self.label_setting_3.setPixmap(QPixmap.fromImage(image4))
    
    @pyqtSlot(QImage, QImage)
    def setImages2(self, image5: QImage, image6: QImage):
        self.label_setting_4.setPixmap(QPixmap.fromImage(image5))
        self.label_setting_5.setPixmap(QPixmap.fromImage(image6))
    
    
    def initUI(self):
        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_0 = QLabel()
        self.label_setting_0.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_0.setScaledContents(True)
        # Первая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_1 = QLabel()
        self.label_setting_1.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_1.setScaledContents(True)
        # Вторая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_4 = QLabel()
        self.label_setting_4.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_4.setScaledContents(True)
        # Вторая картинка --------------------------------------------------

        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_2 = QLabel()
        self.label_setting_2.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_2.setScaledContents(True)
        # Первая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_3 = QLabel()
        self.label_setting_3.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_3.setScaledContents(True)
        # Вторая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_setting_5 = QLabel()
        self.label_setting_5.setMinimumSize(int(self.width()), int(self.height() * 0.2))
        self.label_setting_5.setScaledContents(True)
        # Вторая картинка --------------------------------------------------


        self.v_box_layout_setting_0 = QVBoxLayout()
        self.v_box_layout_setting_0.addWidget(self.label_setting_0, 1)
        self.v_box_layout_setting_0.addWidget(self.label_setting_1, 1)
        self.v_box_layout_setting_0.addWidget(self.label_setting_4, 1)
        
        self.v_box_layout_setting_0.addWidget(self.label_setting_2, 1)
        self.v_box_layout_setting_0.addWidget(self.label_setting_3, 1)
        self.v_box_layout_setting_0.addWidget(self.label_setting_5, 1)
        
        self.setLayout(self.v_box_layout_setting_0)