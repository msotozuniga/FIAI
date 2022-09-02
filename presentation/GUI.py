import settings
import event_functions as ef
import cv2
from presentation.Options import *
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
    
    def setController(self, controller):
        self.controller = controller

    def createMenu(self):
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&Archivo")
        open_action = QAction("Abrir archivo", self)
        open_action.triggered.connect(self.openFile)
        save_action = QAction("guardar archivo", self)
        save_action.triggered.connect(self.sendFileSavedSignal)
        close_action = QAction("Cerrar archivo", self)
        close_action.triggered.connect(self.closeFile)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(close_action)
        self.setMenuBar(self.menu)


    def createWidget(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        self.createLayoutLeft(main_layout)
        self.createLayoutRight(main_layout)
        #TODO continuar
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def createLayoutLeft(self, overall_layout):
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        overall_layout.addLayout(left_layout)
        overall_layout.addLayout(right_layout)

        self.model_option = OptionChoice("Modelo",["BLURIFE","RIFE","SoftSplat"])
        left_layout.addWidget(self.model_option)

        self.device_option = OptionChoice("Dispositivo",["CPU", "GPU"]) #TODO Buscar dispositivos
        left_layout.addWidget(self.device_option)

        self.n_option = OptionNumber("Fotogramas intermedios")
        left_layout.addWidget(self.n_option)

        self.int_frames = OptionRange("Frames a interpolar")
        left_layout.addWidget(self.int_frames)

        int_button = QPushButton("Interpolar")
        int_button.clicked.connect(self.sendInterpolationStartSignal)
        left_layout.addWidget(int_button)

    def createLayoutRight(self, main_layout: QLayout):
        overall_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()

        main_layout.addLayout(overall_layout)
        
        self.image = QLabel("No se ha abierto un video")
        self.image.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        overall_layout.addWidget(self.image)
        
        overall_layout.addLayout(bottom_layout)

        self.frame = QSpinBox()
        self.frame.setMinimum(0) #TODO setear el frame minimo cuando se carga un video
        self.frame.setMaximum(100) #TODO setear frame maximo cuando se carga un video
        self.frame.setSingleStep(1)
        self.frame.setButtonSymbols(QSpinBox.NoButtons)
        self.frame.setValue(1)
        self.frame.valueChanged.connect(self.changeFrame)

        button_left = QPushButton("Anterior")
        button_left.clicked.connect(self.changeFrameBackward)

        button_right = QPushButton("Siguiente")
        button_right.clicked.connect(self.changeFrameForward)

        bottom_layout.addWidget(button_left)
        bottom_layout.addWidget(self.frame)
        bottom_layout.addWidget(button_right)

    def changeFrameBackward(self):
        print(self.frame.value())
        self.changeFrame(self.frame.value()-1)

    def changeFrameForward(self):

        self.changeFrame(self.frame.value()+1)

    def setFrame(self, data):
        frame, value = data
        print(value)
        height, width, channels = frame.shape
        bytesPerLine = 3 * width                                       
        q_img = QImage(frame.data, width, height, bytesPerLine,QImage.Format_RGB888)
        q_pix = QPixmap(q_img)
        print(self.frame.value())
        self.frame.blockSignals(True)
        self.image.setPixmap(q_pix)
        self.frame.setValue(value)
        print(self.frame.value())
        self.frame.blockSignals(False)
        print(self.frame.value())
        
        

        
    def openFile(self):
        file_name = QFileDialog.getOpenFileName(self,"Open File","/home",
                                       "Video (*.avi *.mp4)")
        if file_name[0] != '':
            self.sendFileOpenedSignal(file_name[0])

    def closeFile(self):
        self.sendFileClosedSignal()
        self.close()
        return

    def changeFrame(self, value):
        if value != self.frame.value(): 
            settings.process_queue.put((ef.requestFrame,value,-1))

    def sendFileOpenedSignal(self, file_name):
        settings.process_queue.put((ef.openVideo,file_name, -1))
        
        
    
    def sendFileSavedSignal(self):
        settings.process_queue.put((ef.saveVideo,None, 0))
        

    def sendFileClosedSignal(self):
        settings.process_queue.put((ef.closeProgram,"message", 0))
        return

    def sendInterpolationStartSignal(self):
        data = {}
        data["model"]= self.model_option.selected_option
        data["device"] = self.device_option.selected_option
        data["inbetweens"] = self.n_option.value
        data["frames"]= (self.int_frames.bottom_frame.value,self.int_frames.top_frame.value)
        data["area"]=(None,None,None,None) #TODO agarrar datos
        settings.process_queue.put((ef.interpolate,data, -1))

    
    
    

    
