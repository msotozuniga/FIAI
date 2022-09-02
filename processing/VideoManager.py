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

    def generate_frames(self, lower_left, upper_right, frame_start, frame_end, frames_to_create):
        '''
        frames = self.video[frame_start: frame_end]
        original = frames.copy()
        '''
        left = lower_left[0]
        right = upper_right[0]
        lower = lower_left[1]
        upper = upper_right[1]

        pieces , frames = self.extractor.extract_frames(self.capturer, left,right,lower,upper, frame_start, frame_end)
        self.stitcher.save_frames(frames)
        interpolation = self.model.interpolate(pieces, right - left, upper - lower, frames_to_create)
        results, original= self.stitcher.stitch(interpolation,left,right,lower,upper)
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

    def interpolate(data):
        print("interpolating")
        print(data)
        return

    def get_frame(self,value):
        self.capturer.set(cv2.CAP_PROP_POS_FRAMES,value)
        ret, frame = self.capturer.read()
        if not ret:
            print("not ret") #TODO avisar que el valor es incorrecto
        cv2.cvtColor(frame,cv2.COLOR_BGR2RGB, frame)  
        settings.process_queue.put((ef.responseFrame,frame,1))

