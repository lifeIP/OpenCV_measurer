import sys

from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

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
        
        from src.PageManagerWidget import PageManagerWidget
        self.pageManagerWidget = PageManagerWidget(self.width, self.height)
        
        self.v_box_app_layout = QVBoxLayout()
        self.v_box_app_layout.addWidget(self.pageManagerWidget)
        
        self.setLayout(self.v_box_app_layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())