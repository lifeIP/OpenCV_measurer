from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class DrawCircle(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        print("begin")
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        
        radx = 100
        rady = 100

        paint.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        center = QPoint(120, 120)
        # optionally fill each circle yellow
        paint.setBrush(Qt.white)
        paint.drawEllipse(center, radx, rady)

        print("end")
        paint.end()