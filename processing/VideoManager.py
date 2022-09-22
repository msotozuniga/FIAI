import os

import cv2
import numpy as np
import cv2 as cv #cambiar de cv a pims
import gc
import settings
import event_functions as ef
from deep.RIFE.RIFEWrapper import RIFEWrapper
from deep.SoftSplat.SoftSplatWrapper import SoftSplatWrapper
from deep.BLURIFE.BLURIFEWrapper import BLURIFEWrapper
from processing.VideoData import Videodata



class VideoManager:
    

    def __init__(self):
        '''Constructor de clase
        '''
        self.model = RIFEWrapper()
        self.video = Videodata()
    
    def changeModel(self, model_id):
        '''Define el modelo a usar para interpolar

        Args:
            model_id (int): Identificador del modelo
        '''
        device= self.model.device_system
        if model_id is 0:
            self.model =RIFEWrapper(device_system=device)
        elif model_id is 1:
            self.model = SoftSplatWrapper(device_system=device)
        elif model_id is 2:
            self.model = BLURIFEWrapper(device_system=device)
        

    def openVideo(self, video):
        '''Abre el video a trabajar

        Args:
            video (string): Nombre completo del archivo

        Returns:
            (int,int,int,int): (frame inicial,frame final,ancho,alto)
        '''
        self.video.openVideo(video)
        return self.getVideoData()

    def getVideoData(self):
        '''Solicita de VideoData los metadatos del video

        Returns:
            (int,int,int,int): (frame inicial,frame final,ancho,alto)
        '''
        return self.video.getVideoData()

    def generateFrames(self,left, right, up, down, frame_start, frame_end, frames_to_create):
        '''Envía datos de VideoData al modelo para generar fotogramas

        Args:
            left (int): borde izquierdo de la seccion
            right (itn): borde derecho de la seccion
            up (int): borde superior de la seccion
            down (int): borde inferior de la seccion
            frame_start (int): frame donde comenzar a interpolar
            frame_end (int): frame donde terminar de interpolar
            frames_to_create (int): cantidad de frames a crear entre fotogramas existentes

        Returns:
            (array,int): (primer fotograma creado, numero del fotograma)
        '''
        pieces , frames = self.video.extractFrames(left,right,up,down,frame_start, frame_end)
        self.video.saveFrames(self.video.path_temp,frames)
        self.video.saveMap()
        del frames
        interpolation = self.model.interpolate(pieces, right - left, down - up, frames_to_create)
        result = self.video.stitch(interpolation,left,right,down,up,frames_to_create)
        self.video.loadMap()
        data = self.video.addFrames(result,frame_start,frame_end)
        return data

    def saveVideo(self,data):
        '''Guarda el video creaco

        Args:
            data (str,bool): (Nombre completo archivo, Sobreescribir el archivo)
        '''
        filename,override = data
        self.video.save_video(filename,override)

    def clearCache(self):
        '''Solicita a VideoData que borre los datos no utilizados
        '''
        self.video.clearData()

    def interpolate(self,data):
        '''Recupera los datos dados por el GUI y solitica la creación de frames indicado

        Args:
            data (dict): Datos entregados por GUI: modelo,dispositivo,n de frames a crear, frames a interpolar,area a interpolar

        Returns:
            (array,int): (primer fotograma creado, número del fotograma)
        '''
        model_id = data["model"]
        if model_id != self.model.id:
            self.change_model(model_id)
        device = data["device"]
        if device != self.model.device_system:
            self.model.to_device(device)
        n = data["inbetweens"]
        frame_start, frame_end = data["frames"]
        left,right,up,down = data["area"]
        frame, new_value = self.generateFrames(left,right,up,down,frame_start,frame_end,n)
        cv2.cvtColor(frame,cv2.COLOR_BGR2RGB, frame)
        return (frame, new_value)
        

    def getFrame(self,value):
        '''Solicita a VideoData un fotograma

        Args:
            value (int): Fotograma solicitado

        Returns:
            array: Fotograma pedido
        '''
        return self.video.getFrame(value)

    def deleteFrame(self,value):
        '''Solicita a VideoData que borre in fotograma

        Args:
            value (int): Fotograma a borrar

        Returns:
            array: Fotograma que corresponde al que se ha borrado
        '''
        self.video.deleteFrame(value)
        return self.video.getFrame(value)


