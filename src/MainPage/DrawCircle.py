from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class DrawCircle(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(Qt.white)
        
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 100
        rady = 100
        # draw red circles
        paint.setPen(Qt.red)
        center = QPoint(120, 120)
        # optionally fill each circle yellow
        paint.setBrush(Qt.blue)
        paint.drawEllipse(center, radx, rady)
        paint.end()