import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class MainWindo1w(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.onMyToolBarButtonClick)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(button_action)
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action2)

    def onMyToolBarButtonClick(self, s):
        print("click", s)

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIAI")
        widget = QWidget()
        self.setCentralWidget(widget)
        self.createMenu()

        self.setMinimumSize(720, 480)
        self.setMaximumSize(1920,1080)

    def createMenu(self):
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Archivo")
        open_action = QAction("Abrir archivo", self)
        open_action.triggered.connect(self.openFile)
        save_action = QAction("guardar archivo", self)
        save_action.triggered.connect(self.saveFile)
        close_action = QAction("Cerrar archivo", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        self.setMenuBar(self.menu)
        

    def openFile(self):
        print("opening file")
        return
    
    def saveFile(self):
        print("Saving files")
        return
    
    def closeFile(self):
        print("Closing files")
        self.closeEvent(QCloseEvent())
        return

app = QApplication(sys.argv)
window = Mainwindow()
window.show()

app.exec_()

'''from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import *
import sys

from cv2 import QT_PUSH_BUTTON

app = QApplication(sys.argv)

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIAI")
        self.label = QLabel("Click in this window")
        self.setCentralWidget(self.label)
        self.setMouseTracking(True)


        #self.setMinimumSize(720, 480)
        #self.setMaximumSize(1920,1080)
    
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec_(e.globalPos())
    

window = Mainwindow()
window.show()

app.exec_()
#QFileDialog para abrir el buscador
'''