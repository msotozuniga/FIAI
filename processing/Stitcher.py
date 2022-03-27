import os

import cv2
import numpy as np
import gc
from deep.RIFE.RIFEWrapper import RIFEWrapper

class Stitcher:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path_temp = dir_path + '\\temp\\temp.npy'

    def save_frames(self, frames):
        '''
        Saves the segment in disk
        '''
        with open(self.path_temp, 'wb') as f:
            np.save(f, frames)


    def stitch(self, pieces, left, right, lower, upper):
        frames = np.load(self.path_temp)
        original = np.copy(frames)
        frames[:, left:right, lower:upper] = 0
        frames[1:, left:right, lower:upper] += pieces
        return frames, original

