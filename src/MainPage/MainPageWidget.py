from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class MainPageWidget(QWidget):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.width = width
        self.height = height
        self.initUI()
    
    @pyqtSlot(QImage)
    def setImageOnMainPage(self, image):
        self
        #self.label_main_centering_image.setPixmap(QPixmap.fromImage(image))


    def initUI(self):
        from src.MainPage.DrawCircle import DrawCircle
        circularWidget = DrawCircle()

        self.v_box_layout_centering_widget = QVBoxLayout()
        self.v_box_layout_centering_widget.addWidget(circularWidget)
        self.setLayout(self.v_box_layout_centering_widget)
        