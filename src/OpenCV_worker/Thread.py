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
    addPointOnPlot = pyqtSignal(int)

    @pyqtSlot(int)
    def setTabId(self, id: int):
        self.tab_id = id
    
    @pyqtSlot(int)
    def setFokus_0(self, fokus: int):
        self.cap_0.set(28, fokus)
    
    @pyqtSlot(int)
    def setFokus_1(self, fokus: int):
        self.cap_1.set(28, fokus)
        

    def run(self):
        self.b = 20
        self.g = 80
        self.r = 80
        self.b_1 = 45
        self.g_1 = 255
        self.r_1 = 255

        with open('./settings.netroz') as f:
            data = f.readline()
            self.b = int(data)

            data = f.readline()
            self.g = int(data)

            data = f.readline()
            self.r = int(data)

            data = f.readline()
            self.b_1 = int(data)

            data = f.readline()
            self.g_1 = int(data)

            data = f.readline()
            self.r_1 = int(data)
            
            f.close() 

        self.tab_id = 0

        self.loadingMSG.emit(0)
        self.cap_0 = cv2.VideoCapture(1)
        # self.cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # self.cap0.set(28, 0)

        self.loadingMSG.emit(1)
        self.cap_1 = cv2.VideoCapture(2)
        # self.cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        # self.cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # self.cap1.set(28, 0) 
        self.loadingMSG.emit(2)

        while True:
            ret_0, frame_0 = self.cap_0.read()
            ret_1, frame_1 = self.cap_1.read()

            if frame_0 is None or frame_1 is None: continue

            height_0, width_0 = frame_0.shape[:2]
            # print("width: ", width_0)
            res_h_0 = height_0//2 - 15

            height_1, width_1 = frame_1.shape[:2]
            res_h_1 = height_1//2 - 15

            if ret_0 and ret_1:
                crop_img_0 = frame_0[res_h_0:res_h_0 + 30, 0:0 + width_0]
                crop_img_1 = frame_1[res_h_1:res_h_1 + 30, 0:0 + width_1]
                # cv2.imshow("source", frame_1)

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
                        if(hsv_range_0[j, i] == 255 and diametr_x_start[j] == 0): diametr_x_start[j] = i
                        if(hsv_range_1[j, i] == 255 and diametr_y_start[j] == 0): diametr_y_start[j] = i
                        
                for i in range(width_0 - 1, -1, -1):
                    for j in range(0, 30):
                        if(hsv_range_0[j, i] == 255 and diametr_x_end[j] == 0): diametr_x_end[j] = i
                        if(hsv_range_1[j, i] == 255 and diametr_y_end[j] == 0): diametr_y_end[j] = i

                if self.tab_id == 0:
                    self.changeObjectProperty.emit(int(sum(diametr_x_start)/30), 
                                                   int(sum(diametr_y_start)/30), 
                                                   int((sum(diametr_x_end)/30)-(sum(diametr_x_start)/30)), 
                                                   int((sum(diametr_y_end)/30)-(sum(diametr_y_start)/30)))
                   
                    self.changeDiametr_and_ovality.emit(int((sum(diametr_x_end)/30)-(sum(diametr_x_start)/30))//2, 
                                                    int((sum(diametr_y_end)/30)-(sum(diametr_y_start)/30))/int((sum(diametr_x_end)/30)-(sum(diametr_x_start)/30)))
                    # self.addPointOnPlot.emit((sum(self.diametr_x)/10 + int((sum(diametr_y_end)/30)-int((sum(diametr_x_end)/30)-(sum(diametr_x_start)/30)))
                
                elif self.tab_id == 1:
                    self.objectWidth_x_and_y.emit(int((sum(diametr_x_end)/30)-(sum(diametr_x_start)/30)), 
                                                  int((sum(diametr_y_end)/30)-(sum(diametr_y_start)/30)))
                    self.changeShadowPixmaps.emit(p_0_0, p_1_1)

                elif self.tab_id == 2: 
                    # self.changePixelSize.emit(int(sum(diametr_x_end)/30 - sum(diametr_x_start)/30), int(sum(diametr_y_end)/30 - sum(diametr_y_start)/30))
                    self.changeOriginalPixmaps.emit(p_0, p_1)