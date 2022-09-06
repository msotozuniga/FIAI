import os

import cv2
import numpy as np
import gc
from deep.RIFE.RIFEWrapper import RIFEWrapper

class Stitcher:

    def __init__(self):
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"temp")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        self.path_temp = os.path.join(dir_path,"temp.npy")

    def save_frames(self, frames):
        '''
        Saves the segment in disk
        '''
        np.save(self.path_temp, frames)


    def stitch(self, pieces, left, right, lower, upper, n_frames):
        '''
        Pieces: (n,h,w,c)
        '''
        frames = np.load(self.path_temp) #usar repear en dim 0 para llegar al limite
        frames = np.repeat(frames,n_frames+1,axis=0)[:-1*n_frames]
        original = np.copy(frames)
        frames[:, upper:lower, left:right] = pieces
        if os.path.isfile(self.path_temp):
            os.remove(self.path_temp)
        return frames, original

