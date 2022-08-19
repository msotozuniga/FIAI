from fileinput import filename
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIAI")
        self.createMenu()
        self.createWidget()

        self.setMinimumSize(720, 480)
        self.setMaximumSize(1920,1080)

    def createMenu(self):
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Archivo")
        open_action = QAction("Abrir archivo", self)
        open_action.triggered.connect(self.openFile)
        save_action = QAction("guardar archivo", self)
        save_action.triggered.connect(self.sendFileSavedSignal)
        close_action = QAction("Cerrar archivo", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        self.setMenuBar(self.menu)


    def createWidget(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        #TODO continuar
        self.setCentralWidget(widget)
        

    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self,"Open File","/home",
                                       "Video (*.avi *.mp4)")
        if file_name[0] != '':
            self.sendFileOpenedSignal(file_name[0])

    def sendFileOpenedSignal(self, file_name):
        #TODO
        pass
        
    
    def sendFileSavedSignal(self):
        #TODO
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