import cv2
import numpy as np
from PIL import Image
import time

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

from random import randint

class Thread(QThread):
    changeShadowPixmaps = pyqtSignal(QImage, QImage)
    changeOriginalPixmaps = pyqtSignal(QImage, QImage)
    objectWidth_x_and_y = pyqtSignal(int, int)
    loadingMSG = pyqtSignal(int)
    changeObjectProperty = pyqtSignal(int, int, int, int)
    changeDiametr_and_ovality = pyqtSignal(float, float)

    @pyqtSlot(int)
    def setTabId(self, id: int):
        self.tab_id = id
    
    @pyqtSlot(int)
    def setFokus_0(self, fokus: int):
        self.cap0.set(28, fokus)
    
    @pyqtSlot(int)
    def setFokus_1(self, fokus: int):
        self.cap1.set(28, fokus)
        

    def run(self):
        self.tab_id = 0

        self.loadingMSG.emit(0)
        self.cap0 = cv2.VideoCapture(0)
        self.cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap0.set(28, 0)

        self.loadingMSG.emit(1)
        self.cap1 = cv2.VideoCapture(2)
        self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.cap1.set(28, 0) 
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
                crop_img_0 = self.frame0[self.res_h_0:self.res_h_0 + 30, 0:0 + self.width_0]
                crop_img_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2GRAY)

                crop_img_1 = self.frame1[self.res_h_1:self.res_h_1 + 30, 0:0 + self.width_1]
                crop_img_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2GRAY)
                    
                ret_0, binary_threshold_0 = cv2.threshold(crop_img_0, 127, 255, 0)
                ret_1, binary_threshold_1 = cv2.threshold(crop_img_1, 127, 255, 0)

                cv2.bitwise_not(binary_threshold_0, binary_threshold_0)
                cv2.bitwise_not(binary_threshold_1, binary_threshold_1)

                image0 = cv2.Canny(binary_threshold_0, 70, 135)
                image1 = cv2.Canny(binary_threshold_1, 70, 135)


                height, width = image0.shape
                x_end: int = 0
                for i in range(width):
                    for j in range(height): 
                        if image0[j,i]: x_end = i; break
                
                x_start: int = width
                for i in range(width - 1, -1, -1):
                    for j in range(height -1, -1, -1): 
                        if image0[j,i]: x_start = i; break 

                delta_x_0 = x_end - x_start
                x_end1 = 0
                for i in range(width):
                    for j in range(height): 
                        if image1[j,i]: x_end1 = i; break

                x_start1 = width
                for i in range(width - 1, -1, -1):
                    for j in range(height -1, -1, -1): 
                        if image1[j,i]: x_start1 = i; break
                delta_x_1 = x_end1 - x_start1
                
                a_left_width: int = 0
                d_bottom_height: int = 0

                part_width = width // 2
                if a_left_width < part_width:
                    a_left_width = -(part_width - x_start)
                else:
                    a_left_width = (part_width - x_start)
                
                if d_bottom_height < part_width:
                    d_bottom_height = -(part_width - x_start1)
                else:
                    d_bottom_height = (part_width - x_start1)
                    
                if self.tab_id == 0:
                    self.changeObjectProperty.emit(a_left_width, d_bottom_height, delta_x_0, delta_x_1)
                    self.changeDiametr_and_ovality.emit((delta_x_0+delta_x_1)/2, delta_x_0/delta_x_1)

                elif self.tab_id == 1:
                    self.objectWidth_x_and_y.emit(delta_x_0, delta_x_1)

                    rgbImage_0 = cv2.cvtColor(image0, cv2.COLOR_BGR2RGB)
                    h0, w0, ch0 = rgbImage_0.shape
                    bytesPerLine_0 = ch0 * w0
                    convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                    

                    rgbImage_1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
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
                    h1, w1, ch1 = rgbImage_1.shape
                    bytesPerLine_1 = ch1 * w1
                    convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                    p_1 = convertToQtFormat_1.scaled(300, 250, Qt.KeepAspectRatio)
                    
                    self.changeOriginalPixmaps.emit(p_0, p_1)
                    
