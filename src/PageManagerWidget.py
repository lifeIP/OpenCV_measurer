from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class PageManagerWidget(QWidget):
    def __init__(self, width:int, height:int):
        self.width = width
        self.height = height
        super().__init__()
        self.initUI()

    @pyqtSlot(int)
    def setAnotherStackPage(self, page_id):
        self.stackedLayout.setCurrentIndex(page_id)

    def initUI(self):
        
        from src.OpenCV_worker.Thread import Thread
        th = Thread(self)

        from src.LoadingPage.LoadingPageWidget import LoadingPageWidget
        self.loadingPageWidget = LoadingPageWidget()

        from src.MainPage.MainPageWidget import MainPageWidget
        self.mainPageWidget = MainPageWidget(self.width, self.height)
        
        from src.ShadowViewPage.ShadowViewPageWidget import ShadowViewPageWidget
        self.shadowViewPageWidget = ShadowViewPageWidget(self.width, self.height)

        from src.OriginalViewPage.OriginalViewPageWidget import OriginalViewPageWidget
        self.originalViewPageWidget = OriginalViewPageWidget(self.width, self.height)


        # TabWidget ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tabs = QTabWidget()
        tab0 = self.shadowViewPageWidget
        tab1 = self.originalViewPageWidget
        tab2 = self.mainPageWidget

        v_box_layout_tabs = QVBoxLayout()
        v_box_layout_tabs.addWidget(tabs)
        
        # Add tabs
        tabs.addTab(tab2,"Главная")
        tabs.addTab(tab0,"Тени")
        tabs.addTab(tab1,"Исходники")
        # TabWidget --------------------------------------------------------

        self.tabPagesWidget = QWidget()
        self.tabPagesWidget.setLayout(v_box_layout_tabs)

        self.stackedLayout = QStackedLayout()
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.addWidget(self.loadingPageWidget)
        self.stackedLayout.addWidget(self.tabPagesWidget)
        
        th.changePixmap0.connect(self.shadowViewPageWidget.setImage0)
        th.changePixmap1.connect(self.shadowViewPageWidget.setImage1)
        th.changePixmap2.connect(self.originalViewPageWidget.setImage2)
        th.changePixmap3.connect(self.originalViewPageWidget.setImage3)
        th.objectWidth0.connect(self.shadowViewPageWidget.setDelata_x)
        th.objectWidth1.connect(self.shadowViewPageWidget.setDelata_y)
        th.changeCenteringImage.connect(self.mainPageWidget.setImageOnMainPage)
        self.loadingPageWidget.changeAnotherPage.connect(self.setAnotherStackPage)

        th.loadingMSG.connect(self.loadingPageWidget.setLoadingMSG)
    
        tabs.currentChanged.connect(th.setTabId)

        self.setLayout(self.stackedLayout)
        
        th.start()