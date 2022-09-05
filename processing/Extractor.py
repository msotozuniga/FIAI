import os

import cv2
import numpy as np
import gc
from deep.RIFE.RIFEWrapper import RIFEWrapper

class Extractor:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path_initial = dir_path + '\\temp\\initial.npy'
        self.path_final = dir_path + '\\temp\\final.npy'

    def extract_frames(self, cap, left, right, upper, lower, frame_start, frame_end):
        '''
        Removes the desire segment of video
        :param cap: Video capturer
        :param lower_left: Lower left pixel of segment
        :param upper_right: Upper right pixel of segment
        :param frame_start: Starting frame of segment
        :param frame_end: Ending frame of segment (not included)
        '''
        frames_to_read = frame_end - frame_start
        frames = []
        cap.set(cv2.CAP_PROP_POS_FRAMES,frame_start)
        for i in range(frames_to_read):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        frames = np.stack(frames)
        pieces = frames[:, left:right, upper:lower]
        return pieces, frames


    def save_rest(self, video, frame_start, frame_end):
        initial = video[0:frame_start]
        final = video[frame_end:-1]
        with open(self.path_initial, 'wb') as f:
            np.save(f, initial)
        with open(self.path_final, 'wb') as f:
            np.save(f, final)
        del video
        gc.collect()