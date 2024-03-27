import sys

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    @pyqtSlot(QImage, QImage, QImage, QImage)
    def setImages(self, image: QImage, image2: QImage, image3: QImage, image4: QImage):
        self.label_shadow_0.setPixmap(QPixmap.fromImage(image))
        self.label_shadow_0_0.setPixmap(QPixmap.fromImage(image2))
        self.label_shadow_1.setPixmap(QPixmap.fromImage(image3))
        self.label_shadow_1_1.setPixmap(QPixmap.fromImage(image4))

    @pyqtSlot(int, int)
    def setDelata_x_and_y(self, width_x: int, width_y: int):
        self.label_shadow_0_delta_x.setText("ΔX: " + str(width_x))
        self.label_shadow_1_delta_y.setText("ΔY: " + str(width_y))

    changeColor_0 = pyqtSignal(int)
    changeColor_1 = pyqtSignal(int)
    changeColor_2 = pyqtSignal(int)

    changeColor_0_1 = pyqtSignal(int)
    changeColor_1_1 = pyqtSignal(int)
    changeColor_2_1 = pyqtSignal(int)

    def value_changed_0(self):
        self.changeColor_0.emit(self.slider_0.value())

    def value_changed_1(self):
        self.changeColor_1.emit(self.slider_1.value())

    def value_changed_2(self):
        self.changeColor_2.emit(self.slider_2.value())

    def value_changed_1_0(self):
        self.changeColor_0_1.emit(self.slider_3.value())

    def value_changed_1_1(self):
        self.changeColor_1_1.emit(self.slider_4.value())

    def value_changed_1_2(self):
        self.changeColor_2_1.emit(self.slider_5.value())

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        

        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_0 = QLabel()
        self.label_shadow_0.setMinimumSize(round(self.width * 0.9), round(self.height * 0.2))
        self.label_shadow_0.setScaledContents(True)
        self.label_shadow_0_delta_x = QLabel()
        self.label_shadow_0_delta_x.setText("ΔX: ")
        self.label_shadow_0_delta_x.setMinimumSize(round(self.width * 0.1), round(self.height * 0.2))
        self.h_box_layout_0 = QHBoxLayout()
        self.h_box_layout_0.addWidget(self.label_shadow_0, 9)
        self.h_box_layout_0.addWidget(self.label_shadow_0_delta_x, 1)
        # Первая картинка --------------------------------------------------
        # Первая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_0_0 = QLabel()
        self.label_shadow_0_0.setMinimumSize(int(self.width * 0.9), int(self.height * 0.2))
        self.label_shadow_0_0.setScaledContents(True)
        self.h_box_layout_0_0 = QHBoxLayout()
        self.h_box_layout_0_0.addWidget(self.label_shadow_0_0, 9)
        self.h_box_layout_0_0.addWidget(self.label_shadow_0_delta_x, 1)
        # Первая картинка --------------------------------------------------
        
        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_1 = QLabel()
        self.label_shadow_1.setMinimumSize(int(self.width * 0.9), int(self.height * 0.2))
        self.label_shadow_1.setScaledContents(True)
        self.label_shadow_1_delta_y = QLabel()
        self.label_shadow_1_delta_y.setText("ΔY: ")
        self.label_shadow_1_delta_y.setMinimumSize(int(self.width * 0.1), int(self.height * 0.2))
        self.h_box_layout_1 = QHBoxLayout()
        self.h_box_layout_1.addWidget(self.label_shadow_1, 9)
        self.h_box_layout_1.addWidget(self.label_shadow_1_delta_y, 1)
        # Вторая картинка --------------------------------------------------

        # Вторая картинка ++++++++++++++++++++++++++++++++++++++++++++++++++
        self.label_shadow_1_1 = QLabel()
        self.label_shadow_1_1.setMinimumSize(int(self.width * 0.9), int(self.height * 0.2))
        self.label_shadow_1_1.setScaledContents(True)
        self.h_box_layout_1_1 = QHBoxLayout()
        self.h_box_layout_1_1.addWidget(self.label_shadow_1_1, 9)
        self.h_box_layout_1_1.addWidget(self.label_shadow_1_delta_y, 1)
        # Вторая картинка --------------------------------------------------


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

        self.slider_2 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_2.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_2.setRange(0, 255)
        self.slider_2.setValue(0)
        self.slider_2.setSingleStep(1)
        self.slider_2.valueChanged.connect(self.value_changed_2)

        self.slider_3 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_3.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_3.setRange(0, 255)
        self.slider_3.setValue(0)
        self.slider_3.setSingleStep(1)
        self.slider_3.valueChanged.connect(self.value_changed_1_0)

        self.slider_4 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_4.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_4.setRange(0, 255)
        self.slider_4.setValue(0)
        self.slider_4.setSingleStep(1)
        self.slider_4.valueChanged.connect(self.value_changed_1_1)

        self.slider_5 = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_5.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.slider_5.setRange(0, 255)
        self.slider_5.setValue(0)
        self.slider_5.setSingleStep(1)
        self.slider_5.valueChanged.connect(self.value_changed_1_2)

        self.v_box_layout_0 = QVBoxLayout()
        self.v_box_layout_0.addLayout(self.h_box_layout_0, 1)
        self.v_box_layout_0.addLayout(self.h_box_layout_0_0, 1)
        self.v_box_layout_0.addLayout(self.h_box_layout_1, 1)
        self.v_box_layout_0.addLayout(self.h_box_layout_1_1, 1)
        
        self.v_box_layout_0.addWidget(self.slider_0)
        self.v_box_layout_0.addWidget(self.slider_1)
        self.v_box_layout_0.addWidget(self.slider_2)
        
        self.v_box_layout_0.addWidget(self.slider_3)
        self.v_box_layout_0.addWidget(self.slider_4)
        self.v_box_layout_0.addWidget(self.slider_5)
        
        
        
        self.setLayout(self.v_box_layout_0)

        from AppThread import AppThread
        th = AppThread(self)
        th.changePixmaps.connect(self.setImages)
        th.changePixelSize.connect(self.setDelata_x_and_y)
        self.changeColor_0.connect(th.setColor_0)
        self.changeColor_1.connect(th.setColor_0)
        self.changeColor_2.connect(th.setColor_0)
        self.changeColor_0_1.connect(th.setColor_1_0)
        self.changeColor_1_1.connect(th.setColor_1_1)
        self.changeColor_2_1.connect(th.setColor_1_2)
        th.start()
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())