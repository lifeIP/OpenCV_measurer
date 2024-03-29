from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *


class DrawCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.point_x_pos: int = 0
        self.point_y_pos: int = 0
        self.radius_x: int = 0
        self.radius_y: int = 0



    
    def setObjectProperty(self, a_left_width: int, d_bottom_height: int,
                          e_radius_x:int, f_radius_y: int):
        _old_range = 640
        _new_range = self.height().real - 30

        _a_left_width = int(a_left_width / _old_range * _new_range)
        _d_bottom_height = int(d_bottom_height / _old_range * _new_range)
        _e_radius_x = int(e_radius_x / _old_range * _new_range) // 2
        _f_radius_y = int(f_radius_y / _old_range * _new_range) // 2
        
        # print(_a_left_width, _d_bottom_height, _e_radius_x, _f_radius_y)
        # print(self.width().real, self.height().real)

        self.point_x_pos: int = _a_left_width + _e_radius_x
        self.point_y_pos: int = _d_bottom_height + _f_radius_y
        self.radius_x: int = _e_radius_x
        self.radius_y: int = _f_radius_y
        self.update()
        
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)

        # optional
        paint.setRenderHint(QPainter.Antialiasing)    
        paint.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        center = QPoint(self.width().real//2, self.height().real//2)
        # print("center ", center)
        # optionally fill each circle yellow
        paint.setBrush(Qt.white)
        paint.drawEllipse(center, self.height().real // 2 - 15, self.height().real // 2 - 15)

        paint.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        center2 = QPoint((self.width().real//2 + 15 - self.height().real//2 + self.point_x_pos), (15 + self.point_y_pos))
        paint.drawEllipse(center2, self.radius_x, self.radius_y)

        paint.end()