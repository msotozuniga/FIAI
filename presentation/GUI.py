from re import A
import settings
import event_functions as ef
import cv2
from presentation.Options import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class ImageLabel(QWidget):

    def __init__(self):
        super(ImageLabel,self).__init__()
        layout = QVBoxLayout()
        self.point_one = None
        self.point_two = None
        self.image = None
        self.w=0
        self.h=0
        self.canvas = QLabel("No se ha abierto un video")
        self.canvas.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.canvas.mousePressEvent = self.setFirstPoint
        self.canvas.mouseReleaseEvent = self.setSecondPoint
        self.canvas.mouseDoubleClickEvent = self.deselectPoints
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        app = QApplication.instance()
        self.double_click_interval = app.doubleClickInterval()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        

    def deselectPoints(self,event):
        self.point_one=None
        self.point_two=None
        print(self.point_one)
        print(self.point_two)

    def getEventPoints(self,event):
        x = event.pos().x()
        y = event.pos().y()
        return x, y

    def setFirstPoint(self, event):
        if not self.timer.isActive():
            self.timer.start(self.double_click_interval)
        x,y = self.getEventPoints(event)
        self.point_one = (x,y)
        print(self.point_one)

    def setSecondPoint(self, event):
        if not self.timer.isActive():
            x,y = self.getEventPoints(event)
            self.point_two = (x,y)
            print(self.point_two)
            #TODO crear cuadrado en imagen transparente que cubra la zona seleccionada

    def setFrame(self,image):
        q_pix = QPixmap(image)
        self.canvas.setPixmap(q_pix)

    def setVideoData(self, width,heigth):
        self.w = width
        self.h = heigth

    def getSelectedBorder(self):
        if self.point_one is None or self.point_two is None:
            selection= (self.h,0,0,self.w)
        else:
            x = (self.point_one[0],self.point_two[0])
            y = (self.point_one[1],self.point_two[1])
            selection = (max(y),min(x),min(y),max(x))
        self.point_one = None
        self.point_two = None
        return selection
        
        #TODO hacer que cuando se habra un archivo se le de a este objeto sus dimensiones
        

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

        self.model_option = OptionChoice("Modelo",settings.model_index)
        left_layout.addWidget(self.model_option)

        self.device_option = OptionChoice("Dispositivo",settings.device_index) #TODO Buscar dispositivos
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

        self.image = ImageLabel()

        overall_layout.addWidget(self.image)
        
        overall_layout.addLayout(bottom_layout)

        self.frame = QSpinBox()
        self.frame.setMinimum(0) #TODO setear el frame minimo cuando se carga un video
        self.frame.setMaximum(100) #TODO setear frame maximo cuando se carga un video
        self.frame.setSingleStep(1)
        self.frame.setButtonSymbols(QSpinBox.NoButtons)
        self.frame.setValue(1)
        self.frame.setKeyboardTracking(False)
        self.frame.valueChanged.connect(self.changeFrame)

        button_left = QPushButton("Anterior")
        button_left.clicked.connect(self.changeFrameBackward)

        button_right = QPushButton("Siguiente")
        button_right.clicked.connect(self.changeFrameForward)

        bottom_layout.addWidget(button_left)
        bottom_layout.addWidget(self.frame)
        bottom_layout.addWidget(button_right)
    
    def dummy_function(self,event):
        print(event)


    def changeFrameBackward(self):
        self.changeFrame(self.frame.value()-1)

    def changeFrameForward(self):

        self.changeFrame(self.frame.value()+1)

    def setFrame(self, data):
        frame, value = data
        height, width, channels = frame.shape
        bytesPerLine = 3 * width                                       
        q_img = QImage(frame.data, width, height, bytesPerLine,QImage.Format_RGB888)
        self.image.setFrame(q_img)
        self.frame.blockSignals(True)
        self.frame.setValue(value)
        self.frame.blockSignals(False)
        
    def setVideoData(self, data):
        minimum, maximun, width, height = data
        self.frame.setMinimum(minimum)
        self.frame.setMaximum(maximun)
        self.int_frames.setLimits(minimum,maximun)
        self.image.setVideoData(width,height)

        

        
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
        settings.process_queue.put((ef.requestFrame,value,0))

    def sendFileOpenedSignal(self, file_name):
        settings.process_queue.put((ef.openVideo,file_name, 0))
        
        
    
    def sendFileSavedSignal(self):
        settings.process_queue.put((ef.saveVideo,None, 0))
        

    def sendFileClosedSignal(self):
        settings.process_queue.put((ef.closeProgram,"message", 0))
        return

    def sendInterpolationStartSignal(self):
        data = {}
        data["model"]= self.model_option.getValue()
        data["device"] = self.device_option.getValue()
        data["inbetweens"] = self.n_option.getValue()
        data["frames"]= self.int_frames.getValue()
        data["area"]=self.image.getSelectedBorder()#(None,None,None,None) #(down,left,up,right) TODO agarrar datos
        print(data)
        #settings.process_queue.put((ef.interpolate,data, -1))

    
    
    

    
