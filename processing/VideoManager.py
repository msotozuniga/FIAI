import os

import cv2
import numpy as np
import cv2 as cv #cambiar de cv a pims
import gc
from deep.ModelWrapperAbstract import ModelWrapperAbstract
import settings
import event_functions as ef
from deep.RIFE.RIFEWrapper import RIFEWrapper
from deep.SoftSplat.SoftSplatWrapper import SoftSplatWrapper
from processing.Extractor import Extractor
from processing.Stitcher import Stitcher
from processing.VideoData import Videodata



class VideoManager:
    

    def __init__(self):
        self.model = RIFEWrapper()
        self.extractor = Extractor()
        self.capturer = None
        self.stitcher = Stitcher()
        self.video = Videodata()
    
    def change_model(self, model_id):
        device= self.model.device_system
        if model_id is 0:
            self.model =RIFEWrapper(device_system=device)
        elif model_id is 1:
            self.model = SoftSplatWrapper(device_system=device)
        

    def open_video(self, video):
        '''
        Set the video to work on
        :param video: Video path
        '''
        cap = cv.VideoCapture(video)
        self.capturer = cap
        self.video.open_video(video)
        return self.video.get_video_data()

    def generate_frames(self,left, right, up, down, frame_start, frame_end, frames_to_create):
        '''
        frames = self.video[frame_start: frame_end]
        original = frames.copy()
        '''
        pieces , frames = self.video.extract_frames(left,right,up,down,frame_start, frame_end)
        self.video.save_frames(self.video.path_temp,frames)
        self.video.save_map()
        del frames
        interpolation = self.model.interpolate(pieces, right - left, down - up, frames_to_create)
        result = self.video.stitch(interpolation,left,right,down,up,frames_to_create)
        self.video.load_map()
        data = self.video.add_frames(result,frame_start,frame_end)
        #TODO enviar datos a GUI sobre la nueva cantidad de frames totales
        return data

    def save_video():
        print("Saving video")
        return

    def clear_cache():
        print("Clearing cache")
        return

    def interpolate(self,data):
        model_id = data["model"]
        if model_id != self.model.id:
            self.change_model(model_id)
        device = data["device"]
        if device != self.model.device_system:
            self.model.to_device(device)
        n = data["inbetweens"]
        frame_start, frame_end = data["frames"]
        left,right,up,down = data["area"]
        frame, new_value = self.generate_frames(left,right,up,down,frame_start,frame_end,n)
        cv2.cvtColor(frame,cv2.COLOR_BGR2RGB, frame)
        return (frame, new_value)
        

    def get_frame(self,value):
        return self.video.get_frame(value)

    def delete_frame(self,value):
        self.video.delete_frame(value)
        return self.video.get_frame(value)


