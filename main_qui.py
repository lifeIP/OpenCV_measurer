import cv2
import numpy as np
import time
import sys

from PyQt5.QtWidgets    import QApplication, QWidget, QLabel, QVBoxLayout, QStackedLayout, QHBoxLayout, QTabWidget, QProgressBar
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class Thread(QThread):
    changePixmap0 = pyqtSignal(QImage)
    changePixmap1 = pyqtSignal(QImage)
    changePixmap2 = pyqtSignal(QImage)
    changePixmap3 = pyqtSignal(QImage)
    objectWidth0 = pyqtSignal(int)
    objectWidth1 = pyqtSignal(int)
    loadingMSG = pyqtSignal(int)

    @pyqtSlot(int)
    def setTabId(self, id):
        self.tab_id = id

    def run(self):
        self.tab_id = 0
        self.width = 1
        self.height = 1
        self.loadingMSG.emit(0)
        cap0 = cv2.VideoCapture(0)
        cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        self.loadingMSG.emit(1)
        cap1 = cv2.VideoCapture(1)
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        self.loadingMSG.emit(2)
        ret, image_0 = cap0.read()
        height_0, width_0 = image_0.shape[:2]
        print(height_0, width_0)
        res_h_0 = int(height_0/2) - 15

        ret, image_1 = cap1.read()
        height_1, width_1 = image_1.shape[:2]
        print(height_1, width_1)
        res_h_1 = int(height_1/2) - 15

        self.time_ms = time.time_ns() // 1_000_000
        
        while True:
            
            self.time_ms_p = time.time_ns() // 1_000_000
            if(self.time_ms_p - self.time_ms != 0): print(1000/(self.time_ms_p - self.time_ms))
            self.time_ms = time.time_ns() // 1_000_000


            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            if (ret0 and ret1):

                if self.tab_id == 1:
                    rgbImage_0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
                    h0, w0, ch0 = rgbImage_0.shape
                    bytesPerLine_0 = ch0 * w0
                    convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                    p_0 = convertToQtFormat_0.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap2.emit(p_0)

                    rgbImage_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    h1, w1, ch1 = rgbImage_1.shape
                    bytesPerLine_1 = ch1 * w1
                    convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                    p_1 = convertToQtFormat_1.scaled(640, 480, Qt.KeepAspectRatio)
                    self.changePixmap3.emit(p_1)
                    continue



                crop_img_0 = frame0[res_h_0:res_h_0 + 30, 0:0 + width_0]
                crop_img_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2GRAY)

                crop_img_1 = frame1[res_h_1:res_h_1 + 30, 0:0 + width_1]
                crop_img_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2GRAY)

                ret_0, binary_threshold_0 = cv2.threshold(crop_img_0, 127, 255, cv2.THRESH_BINARY_INV)
                ret_1, binary_threshold_1 = cv2.threshold(crop_img_1, 127, 255, cv2.THRESH_BINARY_INV)

                self.objectWidth0.emit(int(np.sum(binary_threshold_0 == 255)/30))
                self.objectWidth1.emit(int(np.sum(binary_threshold_1 == 255)/30))

                rgbImage_0 = cv2.cvtColor(binary_threshold_0, cv2.COLOR_BGR2RGB)
                h0, w0, ch0 = rgbImage_0.shape
                bytesPerLine_0 = ch0 * w0
                convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                #p_0 = convertToQtFormat_0.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap0.emit(convertToQtFormat_0)


                rgbImage_1 = cv2.cvtColor(binary_threshold_1, cv2.COLOR_BGR2RGB)
                h1, w1, ch1 = rgbImage_1.shape
                bytesPerLine_1 = ch1 * w1
                convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                #p_1 = convertToQtFormat_1.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap1.emit(convertToQtFormat_1)
        

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


class MainPageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        print("Инит")


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
        # Главная вкладка ++++++++++++++++++++++++++++++++++++++++++++++++++
        
        # Главная вкладка --------------------------------------------------

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


class PageManagerWidget(QWidget):
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        super().__init__()
        self.initUI()

    @pyqtSlot(int)
    def setAnotherStackPage(self, page_id):
        self.stackedLayout.setCurrentIndex(page_id)

    def initUI(self):
        
        th = Thread(self)
        self.loadingPageWidget = LoadingPageWidget()
        self.shadowViewPageWidget = ShadowViewPageWidget(self.width, self.height)
        self.originalViewPageWidget = OriginalViewPageWidget(self.width, self.height)


        # TabWidget ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tabs = QTabWidget()
        tab0 = self.shadowViewPageWidget
        tab1 = self.originalViewPageWidget
        
        v_box_layout_tabs = QVBoxLayout()
        v_box_layout_tabs.addWidget(tabs)
        
        # Add tabs
        tabs.addTab(tab0,"Тени")
        tabs.addTab(tab1,"Исходники")
        # TabWidget --------------------------------------------------------

        self.tabPagesWidget = QWidget()
        self.tabPagesWidget.setLayout(v_box_layout_tabs)

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.loadingPageWidget)
        self.stackedLayout.addWidget(self.tabPagesWidget)
        
        th.changePixmap0.connect(self.shadowViewPageWidget.setImage0)
        th.changePixmap1.connect(self.shadowViewPageWidget.setImage1)
        th.changePixmap2.connect(self.originalViewPageWidget.setImage2)
        th.changePixmap3.connect(self.originalViewPageWidget.setImage3)
        th.objectWidth0.connect(self.shadowViewPageWidget.setDelata_x)
        th.objectWidth1.connect(self.shadowViewPageWidget.setDelata_y)
        self.loadingPageWidget.changeAnotherPage.connect(self.setAnotherStackPage)

        th.loadingMSG.connect(self.loadingPageWidget.setLoadingMSG)
    
        tabs.currentChanged.connect(th.setTabId)

        self.setLayout(self.stackedLayout)
        
        th.start()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.pageManagerWidget = PageManagerWidget(self.width, self.height)
        
        self.v_box_app_layout = QVBoxLayout()
        self.v_box_app_layout.addWidget(self.pageManagerWidget)
        
        self.setLayout(self.v_box_app_layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())