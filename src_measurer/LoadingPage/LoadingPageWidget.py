from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class LoadingPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    changeAnotherPage = pyqtSignal(int)

    @pyqtSlot(int)
    def setLoadingMSG(self, msg_id):
        if msg_id == 0:
            self.statusLabel.setText("Идет конфигурация первой камеры")
            self.loadingPageProgressBar.setValue(25)
        elif msg_id == 1:
            self.statusLabel.setText("Идет конфигурация второй камеры")
            self.loadingPageProgressBar.setValue(50)
        elif msg_id == 2:
            self.statusLabel.setText("Приложение готово к работе")
            self.loadingPageProgressBar.setValue(99)
            self.changeAnotherPage.emit(1)

    def initUI(self):
        self.statusLabel = QLabel()

        self.statusLabel.setText("Status")
        self.statusLabel.setStyleSheet("QLabel{font-size: 18pt;}")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        self.loadingPageProgressBar = QProgressBar()
        self.loadingPageProgressBar.setGeometry(30, 40, 200, 25) 

        self.v_box_layout_loading_page = QVBoxLayout()
        self.v_box_layout_loading_page.addWidget(self.statusLabel)
        self.v_box_layout_loading_page.addWidget(self.loadingPageProgressBar)

        self.setLayout(self.v_box_layout_loading_page)
