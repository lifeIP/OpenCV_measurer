from PyQt5.QtWidgets    import *
from PyQt5.QtCore       import *
from PyQt5.QtGui        import *

class PageManagerWidget(QWidget):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        super().__init__()
        self.initUI()

    @pyqtSlot(int)
    def setAnotherStackPage(self, page_id: int):
        self.stackedLayout.setCurrentIndex(page_id)

    def initUI(self):
        
        from src.OpenCV_worker.Thread import Thread
        th = Thread(self)

        from src.LoadingPage.LoadingPageWidget import LoadingPageWidget
        self.loadingPageWidget = LoadingPageWidget()

        from src.MainPage.MainPageWidget import MainPageWidget
        self.mainPageWidget = MainPageWidget()
        
        from src.ShadowViewPage.ShadowViewPageWidget import ShadowViewPageWidget
        self.shadowViewPageWidget = ShadowViewPageWidget()

        from src.OriginalViewPage.OriginalViewPageWidget import OriginalViewPageWidget
        self.originalViewPageWidget = OriginalViewPageWidget()


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
        

        th.changeShadowPixmaps.connect(self.shadowViewPageWidget.setImages)
        th.changeOriginalPixmaps.connect(self.originalViewPageWidget.setImages)
        th.objectWidth_x_and_y.connect(self.shadowViewPageWidget.setDelata_x_and_y)
        th.changeObjectProperty.connect(self.mainPageWidget.setObjectProperty)
        self.loadingPageWidget.changeAnotherPage.connect(self.setAnotherStackPage)
        th.loadingMSG.connect(self.loadingPageWidget.setLoadingMSG)
        th.changeDiametr_and_ovality.connect(self.mainPageWidget.setDiametr_and_ovality)
        th.addPointOnPlot.connect(self.mainPageWidget.addPointOnPlot)
        self.originalViewPageWidget.changeFokus_0.connect(th.setFokus_0)
        self.originalViewPageWidget.changeFokus_1.connect(th.setFokus_1)
        
        tabs.currentChanged.connect(th.setTabId)

        self.setLayout(self.stackedLayout)
        
        th.start()