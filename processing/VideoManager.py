import os

import cv2
import numpy as np
import cv2 as cv #cambiar de cv a pims
import gc
from deep.RIFE.RIFEWrapper import RIFEWrapper


class VideoManager:

    def __init__(self):
        self.model = RIFEWrapper()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.path_initial = dir_path + '\\temp\\initial.npy'
        self.path_final = dir_path + '\\temp\\final.npy'
        self.video = None
        self.extractor = None
        self.stitcher = None

    def open_video(self, video):
        '''
        Loads video in memory
        :param video: Video path
        '''
        cap = cv.VideoCapture(video)
        ret, frame = cap.read()

        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        cv.destroyAllWindows()
        self.video = np.stack(frames)

    def generate_frames(self, lower_left, upper_right, frame_start, frame_end, frames_to_create):
        frames = self.video[frame_start: frame_end]
        original = frames.copy()
        left = lower_left[0]
        right = upper_right[0]
        lower = lower_left[1]
        upper = upper_right[1]
        pieces = frames[:, left:right, lower:upper]
        self.save_rest(frame_start, frame_end)
        results = self.model.interpolate(pieces, right - left, upper - lower, frames_to_create)
        frames[:, left:right, lower:upper] = 0
        frames[1:, left:right, lower:upper]  += results
        return frames[1:,:,:,:], original[1:,:,:,:]

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
