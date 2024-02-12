import cv2
import numpy as np
import time

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

from threading import *

class Thread(QThread):
    changeShadowPixmaps = pyqtSignal(QImage, QImage)
    changeOriginalPixmaps = pyqtSignal(QImage, QImage)

    objectWidth_x_and_y = pyqtSignal(int, int)
    
    loadingMSG = pyqtSignal(int)

    @pyqtSlot(int)
    def setTabId(self, id: int):
        self.tab_id = id

    def run(self):

        self.tab_id = 0

        self.loadingMSG.emit(0)
        cap0 = cv2.VideoCapture(1)
        cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        self.loadingMSG.emit(1)
        cap1 = cv2.VideoCapture(2)
        cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
        cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)
        self.loadingMSG.emit(2)

        ret, image_0 = cap0.read()
        height_0, width_0 = image_0.shape[:2]
        res_h_0 = int(height_0/2) - 15

        ret, image_1 = cap1.read()
        height_1, width_1 = image_1.shape[:2]
        res_h_1 = int(height_1/2) - 15
        
        while True:
            
            ret0, frame0 = cap0.read()
            ret1, frame1 = cap1.read()
            if (ret0 and ret1):
            
                if self.tab_id == 0:
                    ######################################################################
                    self

                elif self.tab_id == 1:
                    crop_img_0 = frame0[res_h_0:res_h_0 + 30, 0:0 + width_0]
                    crop_img_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2GRAY)

                    crop_img_1 = frame1[res_h_1:res_h_1 + 30, 0:0 + width_1]
                    crop_img_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2GRAY)

                    
                    ret_0, binary_threshold_0 = cv2.threshold(crop_img_0, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                    ret_1, binary_threshold_1 = cv2.threshold(crop_img_1, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

                    self.objectWidth_x_and_y.emit(int(np.sum(binary_threshold_0 == 255)/30), int(np.sum(binary_threshold_1 == 255)/30))

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
                    rgbImage_0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
                    h0, w0, ch0 = rgbImage_0.shape
                    bytesPerLine_0 = ch0 * w0
                    convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)

                    rgbImage_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
                    convertToQtFormat_1 = QImage(rgbImage_1.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)

                    self.changeOriginalPixmaps.emit(convertToQtFormat_0, convertToQtFormat_1)
                    continue
