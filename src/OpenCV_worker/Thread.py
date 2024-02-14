import cv2
import numpy as np
import time

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

from random import randint

class Thread(QThread):
    changeShadowPixmaps = pyqtSignal(QImage, QImage)
    changeOriginalPixmaps = pyqtSignal(QImage, QImage)
    objectWidth_x_and_y = pyqtSignal(int, int)
    objectDiametr_and_Ovality = pyqtSignal(float, float)
    loadingMSG = pyqtSignal(int)
    changePointPos = pyqtSignal(int, int)

    @pyqtSlot(int)
    def setTabId(self, id: int):
        print(id)
        self.tab_id = id


    def run(self):
        self.tab_id = 0

        self.loadingMSG.emit(0)
        self.cap0 = cv2.VideoCapture(0, cv2.CAP_V4L)
        self.cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        self.cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        
        self.loadingMSG.emit(1)
        self.cap1 = cv2.VideoCapture(3, cv2.CAP_V4L)
        self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        self.loadingMSG.emit(2)


        while True:
            ret0, self.frame0 = self.cap0.read()
            ret1, self.frame1 = self.cap1.read()
            if self.frame0 is None or self.frame1 is None: continue

            self.height_0, self.width_0 = self.frame0.shape[:2]
            self.res_h_0 = self.height_0//2 - 15

            self.height_1, self.width_1 = self.frame1.shape[:2]
            self.res_h_1 = self.height_1//2 - 15
        
            
            if ret0 and ret1:
                if self.tab_id == 0: self.changePointPos.emit(randint(-12, 12), randint(-12, 12))
                elif self.tab_id == 1:
                    crop_img_0 = self.frame0[self.res_h_0:self.res_h_0 + 30, 0:0 + self.width_0]
                    crop_img_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2GRAY)

                    crop_img_1 = self.frame1[self.res_h_1:self.res_h_1 + 30, 0:0 + self.width_1]
                    crop_img_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2GRAY)

                    
                    ret_0, binary_threshold_0 = cv2.threshold(crop_img_0, 127, 255, 0)
                    ret_1, binary_threshold_1 = cv2.threshold(crop_img_1, 127, 255, 0)

                    self.objectWidth_x_and_y.emit(np.sum(binary_threshold_0 == 0)//30, np.sum(binary_threshold_1 == 0)//30)

                    rgbImage_0 = cv2.cvtColor(binary_threshold_0, cv2.COLOR_BGR2RGB)
                    h0, w0, ch0 = rgbImage_0.shape
                    bytesPerLine_0 = ch0 * w0
                    convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                    

                    rgbImage_1 = cv2.cvtColor(binary_threshold_1, cv2.COLOR_BGR2RGB)
                    h1, w1, ch1 = rgbImage_1.shape
                    bytesPerLine_1 = ch1 * w1
                    convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                    
                    self.changeShadowPixmaps.emit(convertToQtFormat_0, convertToQtFormat_1)


                elif self.tab_id == 2: 
                    rgbImage_0 = cv2.cvtColor(self.frame0, cv2.COLOR_BGR2RGB)
                    h0, w0, ch0 = rgbImage_0.shape
                    bytesPerLine_0 = ch0 * w0
                    convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                    p_0 = convertToQtFormat_0.scaled(300, 250, Qt.KeepAspectRatio)

                    rgbImage_1 = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
                    h1, w1, ch1 = rgbImage_0.shape
                    bytesPerLine_1 = ch1 * w1
                    convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                    p_1 = convertToQtFormat_1.scaled(300, 250, Qt.KeepAspectRatio)
                    self.changeOriginalPixmaps.emit(p_0, p_1)
                    
