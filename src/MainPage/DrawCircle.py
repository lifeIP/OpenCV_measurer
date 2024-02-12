from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class DrawCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.point_x_pos = 9
        self.point_y_pos = -6


    @pyqtSlot(int, int)
    def setPointPos(self, point_x_pos: int, point_y_pos: int):
        self.point_x_pos = point_x_pos
        self.point_y_pos = point_y_pos
        self.update()

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)

        # optional
        paint.setRenderHint(QPainter.Antialiasing)    
        paint.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        center = QPoint(self.width().real//2, self.height().real//2)
        # optionally fill each circle yellow
        paint.setBrush(Qt.white)
        paint.drawEllipse(center, self.height().real // 2 - 15, self.height().real // 2 - 15)

        # Рисование кружка в центре
        if abs(self.point_x_pos) > 8:
            paint.setPen(QPen(Qt.red, 1, Qt.SolidLine))
            paint.drawEllipse(center, 8, 8)
        else: 
            paint.setPen(QPen(Qt.green, 1, Qt.SolidLine))
            paint.drawEllipse(center, 8, 8)

        
        paint.setPen(QPen(Qt.green, 3, Qt.SolidLine))
        paint.drawPoint(QPoint(center.x() + self.point_x_pos, center.y() + self.point_y_pos))

        paint.end()