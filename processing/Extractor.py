import os

import cv2
import numpy as np
import cv2 as cv
import gc
from deep.RIFE.RIFEWrapper import RIFEWrapper

class Extractor:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path_initial = dir_path + '\\temp\\initial.npy'
        self.path_final = dir_path + '\\temp\\final.npy'

    def extract_frames(self, video, lower_left, upper_right, frame_start, frame_end):
        '''
        Removes the desire segment of video
        :param video: Video matrix
        :param lower_left: Lower left pixel of segment
        :param upper_right: Upper right pixel of segment
        :param frame_start: Starting frame of segment
        :param frame_end: Ending frame of segmente (not included)
        '''
        frames = video[frame_start: frame_end]
        left = lower_left[0]
        right = upper_right[0]
        lower = lower_left[1]
        upper = upper_right[1]
        pieces = frames[:, left:right, lower:upper]
        return pieces


    def save_rest(self, video, frame_start, frame_end):
        initial = video[0:frame_start]
        final = video[frame_end:-1]
        with open(self.path_initial, 'wb') as f:
            np.save(f, initial)
        with open(self.path_final, 'wb') as f:
            np.save(f, final)
        del video
        gc.collect()