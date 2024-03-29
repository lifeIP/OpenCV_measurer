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

    changeFokus_0 = pyqtSignal(int)
    changeFokus_1 = pyqtSignal(int)
    

    def value_changed_0(self):
        self.changeFokus_0.emit(self.slider_0.value())

    def value_changed_1(self):
        self.changeFokus_1.emit(self.slider_1.value())

    def initUI(self):
        # Вторая вкладка +++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_2 = QLabel()
        self.label_shadow_2.setMinimumSize(int(self.width() * 0.95), int(self.height() * 0.5))
        self.label_shadow_2.setScaledContents(True)
        
        self.label_shadow_3 = QLabel()
        self.label_shadow_3.setMinimumSize(int(self.width() * 0.95), int(self.height() * 0.5))
        self.label_shadow_3.setScaledContents(True)

        self.slider_0 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_0.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_0.setRange(0, 255)
        self.slider_0.setValue(0)
        self.slider_0.setSingleStep(1)
        self.slider_0.valueChanged.connect(self.value_changed_0)

        self.slider_1 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_1.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_1.setRange(0, 255)
        self.slider_1.setValue(0)
        self.slider_1.setSingleStep(1)
        self.slider_1.valueChanged.connect(self.value_changed_1)

        # Вторая вкладка ---------------------------------------------------
        v_box_layout_tab_1 = QVBoxLayout()
        v_box_layout_tab_1.addWidget(self.label_shadow_2)
        v_box_layout_tab_1.addWidget(self.slider_0)
        v_box_layout_tab_1.addWidget(self.label_shadow_3)
        v_box_layout_tab_1.addWidget(self.slider_1)
        self.setLayout(v_box_layout_tab_1)
