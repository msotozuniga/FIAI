import sys
from Options import *
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
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.model_option = OptionChoice("Modelo",["BLURIFE","RIFE","SoftSplat"])
        left_layout.addWidget(self.model_option)

        self.device_option = OptionChoice("Dispositivo",["CPU", "GPU"]) #TODO Buscar dispositivos
        left_layout.addWidget(self.device_option)

        self.n_option = OptionNumber("Fotogramas intermedios")
        left_layout.addWidget(self.n_option)
        #TODO continuar
        widget.setLayout(main_layout)
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