import os

import cv2
import numpy as np
import cv2 as cv #cambiar de cv a pims
import gc
import settings
import event_functions as ef
from deep.RIFE.RIFEWrapper import RIFEWrapper
from deep.SoftSplat.SoftSplatWrapper import SoftSplatWrapper
from processing.Extractor import Extractor
from processing.Stitcher import Stitcher



class VideoManager:

    def __init__(self):
        self.model = RIFEWrapper()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path_initial = dir_path + '\\temp\\initial.npy'
        self.path_final = dir_path + '\\temp\\final.npy'
        self.extractor = Extractor()
        self.capturer = None
        self.stitcher = Stitcher()
        self.fps = None
        self.frame_count = None
    
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
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH ))   # float `width`
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
        return (0, self.frame_count, width,height)

    def generate_frames(self,left, right, up, down, frame_start, frame_end, frames_to_create):
        '''
        frames = self.video[frame_start: frame_end]
        original = frames.copy()
        '''

        pieces , frames = self.extractor.extract_frames(self.capturer, left,right,up,down, frame_start, frame_end)
        self.stitcher.save_frames(frames)
        del frames
        interpolation = self.model.interpolate(pieces, right - left, down - up, frames_to_create)
        results, original= self.stitcher.stitch(interpolation,left,right,down,up)
        return results, original


    def save_rest(self, frame_start, frame_end):
        #Usar un compressor
        initial = self.video[0:frame_start]
        final = self.video[frame_end + 1:-1]
        with open(self.path_initial, 'wb') as f:
            np.savez_compressed(f, initial)
        with open(self.path_final, 'wb') as f:
            np.savez_compressed(f, final)
        del self.video
        gc.collect()

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
        result, original = self.generate_frames(left,right,up,down,frame_start,frame_end,n)
        

        


        print("interpolating")
        print(data)
        return

    def get_frame(self,value):
        #TODO Hacer que funcione cuando se coloquen otros frames
        self.capturer.set(cv2.CAP_PROP_POS_FRAMES,value)
        ret, frame = self.capturer.read()
        if not ret:
            return (None,-1)
        cv2.cvtColor(frame,cv2.COLOR_BGR2RGB, frame)
        return (frame,value)

