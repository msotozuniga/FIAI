from xml.dom.minidom import Element
import cv2 as cv
import numpy as np
import os
import uuid
import pickle


class Frame:
    '''Clase abstracta para representar fotogramas
    '''

    def __init__(self, internal_frame,type):
        '''Contructor de clase

        Args:
            internal_frame (int): Fotograma interno del stube
            type (int): id del tipo de frame
        ''' 
        self.i_frame = internal_frame
        self.type = type

    def equalType(self,obj):
        '''Verifica si dos tipos son iguales

        Args:
            obj (obj): objeto a comparar    

        Returns:
            bool: si los objetos son mismo tipo
        '''
        return type(self) is type(obj)

class VideoFrame(Frame):
    '''Clase para representar un fotograma que proviene del video
    '''

    def __init__(self, internal_frame):
        '''Costructor frame de video

        Args:
            internal_frame (int): frame interno del video
        '''
        super().__init__(internal_frame, 0)

    def getFrame(self,cap):
        '''Obtiene fotograma del video abierto

        Args:
            cap (VideoCapturer): capturadora de video

        Returns:
            array: Frame asociado al objeto
        '''
        cap.set(cv.CAP_PROP_POS_FRAMES,self.i_frame)
        ret, frame = cap.read()
        if not ret:
            return (None,-1)
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return frame

    @staticmethod
    def extract_frames(left, right, upper, lower, frame_start, frame_end,cap):
        '''Extrae frames de una sección del video

        Args:
            left (int): borde izq
            right (int): borde derecho
            upper (int): borde superior
            lower (int): borde inferior
            frame_start (int): primera frame a sacar    
            frame_end (int): ultimo frame a ver    
            cap (VideoCapturer): capturadora de video

        Returns:
            (array,array,bool): (secciones, fotogramas correspondientes a secciones, Si la función se ejecuto)
        '''
        if frame_start ==None or frame_end ==None:
            return None,None, True
        frames_to_read = frame_end - frame_start +1 
        frames = []
        cap.set(cv.CAP_PROP_POS_FRAMES,frame_start)
        for i in range(frames_to_read):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        frames = np.stack(frames)
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames, False
        

class StubFrame(Frame):

    def __init__(self, internal_frame, filename):
        '''Constructor para stubs de video

        Args:
            internal_frame (int): frame interno del stub
            filename (str): nombre del stub
        '''
        super().__init__(internal_frame, 1)
        self.file_name = filename

    def getFrame(self):
        '''Obtiene fotograma del video abierto

        Args:
            cap (VideoCapturer): capturadora de video

        Returns:
            array: Frame asociado al objeto
        '''
        frames = np.load(self.file_name)
        frame = frames[self.i_frame]
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return frame


    def equalType(self, obj):
        '''Verifica si el objeto corresponde al mismo stub

        Args:
            obj (obj): Objeto a comparar

        Returns:
            bool: Si los objetos corresponden al mismo stub
        '''
        temp =  super().equalType(obj)
        if temp:
            return self.file_name ==obj.file_name
        return temp

    @staticmethod
    def extract_frames(left, right, upper, lower, frame_start, frame_end,file_name):
        '''Extrae frames de una sección del video

        Args:
            left (int): borde izq
            right (int): borde derecho
            upper (int): borde superior
            lower (int): borde inferior
            frame_start (int): primera frame a sacar    
            frame_end (int): ultimo frame a ver    
            file_name (str): nombre completo del stub

        Returns:
            (array,array,bool): (secciones, fotogramas correspondientes a secciones, Si la función se ejecuto)
        '''
        if frame_start ==None or frame_end ==None:
            return None,None, True
        frames = np.load(file_name)
        frames = frames[frame_start:frame_end+1]
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames, False

class Videodata:

    def __init__(self):
        '''Constructor de los datos del video
        '''
        self.capturer = None
        self.fps = None
        self.frame_count = None
        self.frame_map = []
        self.stubs =[]
        self.width = None
        self.height = None
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"temp")
        self.map_path = os.path.join(self.dir_path,"map.bn")
        self.path_temp = os.path.join(self.dir_path,"temp.npy")
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)

    def openVideo(self, video):
        '''Carga los metadatos del video y setea variables iniciales

        Args:
            video (str): nombre del video
        '''
        cap = cv.VideoCapture(video)
        self.capturer = cap
        self.fps = cap.get(cv.CAP_PROP_FPS)
        self.frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH ))   # float `width`
        self.height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_map = []
        for frame_id in range(int(self.frame_count)):
            frame_map.append(VideoFrame(frame_id))
        self.frame_map = frame_map

    def getVideoData(self):
        '''Obtiene los metadatos del video

        Returns:
            (int,int,int,int): (frame inicial,frames totales,ancho,alto)
        '''
        return (0, self.frame_count, self.width ,self.height)

    def getFrame(self,value):
        '''Obtiene un frame del video total.
        Si no se puede obtener, retorna nada y un numero de frame negativo

        Args:
            value (int): frame solicitado

        Returns:
            (array,int): (frame,numero del frame)
        '''
        try:
            frame= self.frame_map[value]
        except:
            return None, -1
        if type(frame) is VideoFrame:
            data = frame.getFrame(self.capturer)
        else:
            data = frame.getFrame()
        return data, value

    def deleteFrame(self,value):
        '''Borra un frame

        Args:
            value (int): frame a borrar
        '''
        self.frame_map.pop(value)
        self.frame_count-=1

    def saveMap(self):
        '''Guarda el mapa de frames en memoria de disco
        '''
        with open(self.map_path, "wb") as fp:   #Pickling
            pickle.dump(self.frame_map, fp)
        self.frame_map = None

    def loadMap(self):
        '''Carga el mapa de frames en memoria RAM
        '''
        with open(self.map_path, "rb") as fp:   #Pickling
            self.frame_map = pickle.load(fp)
        if os.path.isfile(self.map_path):
            os.remove(self.map_path)
        

    def clearData(self):
        '''Elimina los stubs temporales creados
        '''
        for file in self.stubs:
            if os.path.isfile(file):
                os.remove(file)
        self.__init__()
                



    

    def stitch(self, pieces, left, right, lower, upper, n_frames):
        '''Pega una seccion de video interpolada con los frames correspondientes

        Args:
            pieces (array): secciones de frames
            left (int): borde izquierdo
            right (int): borde derecho
            lower (int): borde inferior
            upper (int): borde superior
            n_frames (int): cantidad de frames creado entre par

        Returns:
            array: frames de tamaño completo con secciones interpoladas
        '''
        frames = np.load(self.path_temp) #usar repear en dim 0 para llegar al limite
        frames = np.repeat(frames,n_frames+1,axis=0)[:-1*(n_frames+1)]
        frames[:, upper:lower, left:right] = pieces
        if os.path.isfile(self.path_temp):
            os.remove(self.path_temp)
        return frames


    def extractFrames(self, left,right,up,down, frame_start, frame_end):
        '''Extrae piezas de los fotogramas a interpolar

        Args:
            left (int): borde izquierdo
            right (int): borde derecho
            up (int): borde superior
            down (int): borde inferior
            frame_start (int): primer frame a interpolar
            frame_end (int): ultimo frame a interpolar

        Returns:
            (array,array): (secciones extraídas, frames originales)
        '''
        curr_obj = self.frame_map[frame_start]
        curr_type = type(curr_obj)
        curr_add_on = curr_obj.file_name if curr_type is StubFrame else self.capturer
        curr_interval = [curr_obj.i_frame,curr_obj.i_frame]
        frames_sets =[]
        pieces_sets = []
        for i in range(frame_start+1,frame_end+1):
            element = self.frame_map[i]
            if not element.equalType(curr_obj) or element.i_frame > curr_obj.i_frame+1:
                piece,frame, empty =curr_type.extract_frames(left, right, up, down, curr_interval[0],curr_interval[1],curr_add_on)
                if not empty:
                    pieces_sets.append(piece)
                    frames_sets.append(frame)
                curr_type = type(element)
                curr_obj = element
                curr_add_on = element.file_name if curr_type is StubFrame else self.capturer
                curr_interval[0] = element.i_frame
            curr_interval[1]=element.i_frame
        piece,frame, empty =curr_type.extract_frames(left, right, up, down, curr_interval[0],curr_interval[1],curr_add_on) 
        if not empty:
            pieces_sets.append(piece)
            frames_sets.append(frame)  
        todas_pieces = np.concatenate(pieces_sets[:],axis=0)
        todas_frames = np.concatenate(frames_sets[:],axis=0)
        return todas_pieces,todas_frames

    def insertFrames(self, stub_name,frames_added, l,r):
        '''Inserta frames interpolados al mapa de frames

        Args:
            stub_name (str): nombre del stub donde guardar los frames
            frames_added (int): frames creados
            l (int): indice donde se debe insertar los frames
            r (int): indice donde terminan los frames insertados
        '''
        for i in range(r-l):
            self.frame_map.pop(l)
        index = l
        for i in range(frames_added):
            stub_frame = StubFrame(i,stub_name)
            self.frame_map.insert(index,stub_frame)
            index +=1

    def addFrames(self, result, frame_start,frame_end):
        '''Añade los frames interpolados al video

        Args:
            result (array): frames interpolados
            frame_start (int): indice donde se debe insertar los frames
            frame_end (int): indice donde terminan los frames insertados

        Returns:
            (array,int): (primer frame interpolado, numero de frame)
        '''
        frames_added,_,_,_ = result.shape
        file_id = uuid.uuid4().hex[:10].upper() + ".npy"
        stub_path = os.path.join(self.dir_path,file_id)
        self.stubs.append(stub_path)
        self.saveFrames(stub_path,result)
        self.insertFrames(stub_path,frames_added,frame_start,frame_end)
        self.frame_count = self.frame_count + frames_added - (frame_end-frame_start)
        return result[1], frame_start+1

    def saveVideo(self,filename,override):
        '''Compila el video en la ubicacion dada

        Args:
            filename (str): nombre del archivo
            override (bool): Indica si se debe sobreescribir un archivo
        '''
        path_to_save = filename
        if override:
            filename, file_extension = os.path.splitext(filename)
            temporal_file = "temp."+file_extension
            path_to_save = os.path.join(self.dir_path,temporal_file)
        video = cv.VideoWriter(path_to_save,cv.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width,self.height))
        for i in range(int(self.frame_count)):
            frame , value = self.getFrame(i)
            cv.cvtColor(frame,cv.COLOR_RGB2BGR, frame)
            if value>=0:
                video.write(frame)
        video.release()
        print("Finaliza el guardado")
          
        

    @staticmethod
    def saveFrames(path, frames):
        '''Guarda frames en un archivo en disco

        Args:
            path (str): ubicacion donde guardar
            frames (array): frames a guardar
        '''
        np.save(path, frames)
        




