import cv2
import numpy as np
from PIL import Image
import time

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class AppThread(QThread):

    changePixmaps = pyqtSignal(QImage, QImage, QImage, QImage)
    changePixelSize = pyqtSignal(int, int)

    @pyqtSlot(int)
    def setColor_0(self, color: int):
        self.b = color;

    @pyqtSlot(int)
    def setColor_1(self, color: int):
        self.g = color;
    
    @pyqtSlot(int)
    def setColor_2(self, color: int):
        self.r = color;


    @pyqtSlot(int)
    def setColor_1_0(self, color: int):
        self.b_1 = color;

    @pyqtSlot(int)
    def setColor_1_1(self, color: int):
        self.g_1 = color;
    
    @pyqtSlot(int)
    def setColor_1_2(self, color: int):
        self.r_1 = color;
    
    def run(self):
        # (20, 80, 80), (45, 255, 255)
        self.b = 20
        self.g = 80
        self.r = 80
        self.b_1 = 45
        self.g_1 = 255
        self.r_1 = 255
        cap_0 = cv2.VideoCapture(0)
        cap_1 = cv2.VideoCapture(1)
        # Посылаем сигнал
        while(True):
            ret_0, frame_0 = cap_0.read()
            ret_1, frame_1 = cap_1.read()

            if frame_0 is None or frame_1 is None: continue

            height_0, width_0 = frame_0.shape[:2]
            res_h_0 = height_0//2 - 15

            height_1, width_1 = frame_1.shape[:2]
            res_h_1 = height_1//2 - 15

            if ret_0 and ret_1:
                crop_img_0 = frame_0[res_h_0:res_h_0 + 30, 0:0 + width_0]
                crop_img_1 = frame_1[res_h_1:res_h_1 + 30, 0:0 + width_1]
                cv2.imshow("source", frame_1)

                hsv_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2HSV)
                hsv_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2HSV)


                # hsv_range_0 = cv2.inRange(hsv_0, (20, 80, 80), (45, 255, 255))
                # hsv_range_1 = cv2.inRange(hsv_1, (20, 80, 80), (45, 255, 255))
                hsv_range_0 = cv2.inRange(hsv_0, (self.b, self.g, self.r), (self.b_1, self.g_1, self.r_1))
                hsv_range_1 = cv2.inRange(hsv_1, (self.b, self.g, self.r), (self.b_1, self.g_1, self.r_1))

                frame_0_0 = crop_img_0.copy()
                frame_1_1 = crop_img_1.copy()

                frame_0_0[hsv_range_0==255] = (0,0,255)
                frame_1_1[hsv_range_1==255] = (0,0,255)

                

                rgbImage_0 = cv2.cvtColor(crop_img_0, cv2.COLOR_BGR2RGB)
                h0, w0, ch0 = rgbImage_0.shape
                bytesPerLine_0 = ch0 * w0
                convertToQtFormat_0 = QImage(rgbImage_0.data, w0, h0, bytesPerLine_0, QImage.Format_RGB888)
                p_0 = convertToQtFormat_0.scaled(300, 250, Qt.KeepAspectRatio)


                rgbImage_0_0 = cv2.cvtColor(frame_0_0, cv2.COLOR_BGR2RGB)
                h0_0, w0_0, ch0_0 = rgbImage_0_0.shape
                bytesPerLine_0_0 = ch0_0 * w0_0
                convertToQtFormat_0_0 = QImage(rgbImage_0_0.data, w0_0, h0_0, bytesPerLine_0_0, QImage.Format_RGB888)
                p_0_0 = convertToQtFormat_0_0.scaled(300, 250, Qt.KeepAspectRatio)


                rgbImage_1 = cv2.cvtColor(crop_img_1, cv2.COLOR_BGR2RGB)
                h1, w1, ch1 = rgbImage_1.shape
                bytesPerLine_1 = ch1 * w1
                convertToQtFormat_1 = QImage(rgbImage_1.data, w1, h1, bytesPerLine_1, QImage.Format_RGB888)
                p_1 = convertToQtFormat_1.scaled(300, 250, Qt.KeepAspectRatio)


                rgbImage_1_1 = cv2.cvtColor(frame_1_1, cv2.COLOR_BGR2RGB)
                h1_1, w1_1, ch1_1 = rgbImage_1_1.shape
                bytesPerLine_1_1 = ch1_1 * w1_1
                convertToQtFormat_1_1 = QImage(rgbImage_1_1.data, w1_1, h1_1, bytesPerLine_1_1, QImage.Format_RGB888)
                p_1_1 = convertToQtFormat_1_1.scaled(300, 250, Qt.KeepAspectRatio)

                self.changePixmaps.emit(p_0, p_0_0, p_1, p_1_1)

                diametr_x_start =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                diametr_x_end =     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                diametr_y_start =   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                diametr_y_end =     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

                for i in range(0, width_0):
                    for j in range(0, 30):
                        # if(hsv_range_0[i, j] == 255 and diametr_x_start[j] == 0): diametr_x_start[j] = i
                        if(hsv_range_1[j, i] == 255 and diametr_y_start[j] == 0): diametr_y_start[j] = i
                        
                for i in range(width_0 - 1, -1, -1):
                    for j in range(0, 30):
                        # if(hsv_range_0[i, j] == 255 and diametr_x_end[j] == 0): diametr_x_end[j] = i
                        if(hsv_range_1[j, i] == 255 and diametr_y_end[j] == 0): diametr_y_end[j] = i

                print("sum")        
                print(sum(diametr_y_end)/30, sum(diametr_y_start)/30)
                
                self.changePixelSize.emit(int(sum(diametr_x_end)/30 - sum(diametr_x_start)/30), int(sum(diametr_y_end)/30 - sum(diametr_y_start)/30))