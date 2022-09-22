from re import A
import settings
import event_functions as ef
import cv2
from presentation.Options import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class HelpWindow(QWidget):

    def __init__(self, parent):
        super(HelpWindow,self).__init__()
        layout = QVBoxLayout()

        title = QLabel("Manual de usuario")
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(title)

        man = """Controles para imagen:\n 
        click+drag: Seleccionar sección de vídeo \n 
        doble click: Borrar selección\n

        Si no hay una sección a interpolar se realizará con toda la imagen
        """
        label = QLabel(man)
        label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(label)

        del_button = QPushButton("Cerrar")
        del_button.clicked.connect(self.close)
        layout.addWidget(del_button)



        self.setLayout(layout)
        self.setWindowTitle("Manual de usuario")
        self.setMinimumSize(500, 480)
        self.caller = parent 

    def closeEvent(self, event):
        self.caller.w=None
        event.accept() # let the window close


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
        self.canvas.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.canvas.setScaledContents(False)
        self.canvas.mousePressEvent = self.setFirstPoint
        self.canvas.mouseReleaseEvent = self.setSecondPoint
        self.canvas.mouseDoubleClickEvent = self.deselectPoints
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.rubberBand = None
        app = QApplication.instance()
        self.double_click_interval = app.doubleClickInterval()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        

    def deselectPoints(self,event):
        self.point_one=None
        self.point_two=None
        self.rubberBand.hide()
        print(self.point_one)
        print(self.point_two)

    def getEventPoints(self,event):
        x = event.pos().x()
        y = event.pos().y()
        return x, y

    def setFirstPoint(self, event):
        if not self.timer.isActive():
            self.timer.start(self.double_click_interval)
        
        self.point_one = event.pos()
        self.point_two = None
        self.origin = self.point_one + self.canvas.pos()
        if not self.rubberBand:
            self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        
        

    def setSecondPoint(self, event):
        if not self.timer.isActive():
            self.point_two = event.pos()
        else:
            self.rubberBand.hide()

    def setFrame(self,image):
        q_pix = QPixmap(image)
        self.canvas.setPixmap(q_pix)

    def setVideoData(self, width,heigth):
        self.w = width
        self.h = heigth


    def getSelectedBorder(self):
        if self.point_one is None or self.point_two is None:
            selection= (0,self.w,0,self.h)
        else:
            p_s_i, p_i_d = self.getRectangle(self.point_one,self.point_two)
            selection = (max(p_s_i.x(),0),min(p_i_d.x(),self.w),max(p_s_i.y(),0),min(p_i_d.y(),self.h))
        self.point_one = None
        self.point_two = None
        return selection

    def mouseMoveEvent(self, event):
        p_a, p_b = self.getRectangle(self.origin, event.pos())
        self.rubberBand.setGeometry(QRect(p_a, p_b))
        self.rubberBand.show()

    @staticmethod
    def getRectangle(point_a, point_b):
        x = point_a.x(), point_b.x()
        y = point_a.y(), point_b.y()
        return QPoint(min(x),min(y)), QPoint(max(x),max(y))
        

class Mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FIAI")
        self.createMenu()
        self.createWidget()
        self.file_name = None
        self.w =None
        self.setMinimumSize(720, 480)
        self.showMaximized()
    
    def setController(self, controller):
        self.controller = controller

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
        help_menu = self.menu.addMenu("Ayuda")
        open_man = QAction("Manual de usuario", self)
        open_man.triggered.connect(self.showHelpWindow)
        help_menu.addAction(open_man)
        self.setMenuBar(self.menu)


    def createWidget(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        self.createLayoutLeft(main_layout)
        self.createLayoutRight(main_layout)
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

        del_button = QPushButton("Borrar frame")
        del_button.clicked.connect(self.sendDeleteFrameSignal)

        button_left = QPushButton("Anterior")
        button_left.clicked.connect(self.changeFrameBackward)

        button_right = QPushButton("Siguiente")
        button_right.clicked.connect(self.changeFrameForward)

        bottom_layout.addWidget(button_left)
        bottom_layout.addWidget(self.frame)
        bottom_layout.addWidget(del_button)
        bottom_layout.addWidget(button_right)

    
    def showHelpWindow(self):
        if self.w is None:
            self.w = HelpWindow(self)
            self.w.show()
        else:
            self.w.close()  # Close window.
            self.w = None  # Discard reference.

    def changeFrameBackward(self):
        self.changeFrame(self.frame.value()-1)

    def changeFrameForward(self):

        self.changeFrame(self.frame.value()+1)

    def setFrame(self, data):
        frame, value = data
        if value == -1:
            print("Valor incorrecto")
            return
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
            self.file_name = file_name[0]

    def saveFile(self):
        if not self.checkActive():
            return
        file_name = QFileDialog.getSaveFileName(self,"Save File",self.file_name,
                                       "AVI (*.avi);;Mp4 (*.mp4)")
        if file_name[0] == '':
            return
        override=False
        if file_name[0]==self.file_name:
            override = True
            print("Se sobreescribirá el archivo")
        self.sendFileSavedSignal(file_name[0], override)



    def closeEvent(self, event):
        self.sendFileClosedSignal()
        event.accept() # let the window close
        

    def changeFrame(self, value):
        settings.process_queue.put((ef.requestFrame,value,0))

    def sendFileOpenedSignal(self, file_name):
        settings.process_queue.put((ef.openVideo,file_name, 0))
        
        
    
    def sendFileSavedSignal(self,filename,override):
        settings.process_queue.put((ef.saveVideo,(filename,override), 0))
        

    def sendFileClosedSignal(self):
        if self.checkActive:
            settings.process_queue.put((ef.closeProgram,"message", 0))

    def sendInterpolationStartSignal(self):
        data = {}
        data["model"]= self.model_option.getValue()
        data["device"] = self.device_option.getValue()
        data["inbetweens"] = self.n_option.getValue()
        data["frames"]= self.int_frames.getValue()
        data["area"]=self.image.getSelectedBorder()
        settings.process_queue.put((ef.interpolate,data, 0))

    def sendDeleteFrameSignal(self):
        settings.process_queue.put((ef.deleteFrame,self.frame.value(), 0))

    def checkActive(self):
        return self.file_name != None


    
    
    

    
