import cv2 as cv
import numpy as np

class IntervalAbstract:

    def __init__(self,l,r,i_l, i_r):
        self.g_l= l
        self.g_r =r
        self.i_l = i_l
        self.i_r = i_r

    def extract_frames(self,left, right, upper, lower, frame_start, frame_end):
        pass

    def get_frame(self,value):
        pass

class VideoInterval(IntervalAbstract):

    def __init__(self, l, r, i_l, i_r,cap):
        super().__init__( l, r, i_l, i_r)
        self.cap =cap

    def extract_frames(self, left, right, upper, lower, frame_start, frame_end):
        '''
        Removes the desire segment of video
        :param cap: Video capturer
        :param lower_left: Lower left pixel of segment
        :param upper_right: Upper right pixel of segment
        :param frame_start: Starting global frame of segment
        :param frame_end: Ending global frame of segment 
        '''
        super().extract_frames(left, right, upper, lower, frame_start, frame_end)
        frames_to_read = frame_end - frame_start +1 
        firs_pos = frame_start-self.g_l+self.i_l
        frames = []
        self.cap.set(cv.CAP_PROP_POS_FRAMES,firs_pos)
        for i in range(frames_to_read):
            ret, frame = self.cap.read()
            if not ret:
                break
            frames.append(frame)
        frames = np.stack(frames)
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames

    def get_frame(self,value):
        firs_pos = value-self.g_l+self.i_l
        self.capturer.set(cv.CAP_PROP_POS_FRAMES,firs_pos)
        ret, frame = self.capturer.read()
        if not ret:
            return (None,-1)
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return (frame,value)

class GroupInterval(IntervalAbstract):

    def __init__(self, l, r, i_l, i_r, file_name):
        super().__init__(l, r, i_l, i_r, next)
        self.file_name = file_name

    def extract_frames(self, left, right, upper, lower, frame_start, frame_end):
        '''''
        Removes the desire segment of video
        :param lower_left: Lower left pixel of segment
        :param upper_right: Upper right pixel of segment
        :param frame_start: Starting global frame of segment
        :param frame_end: Ending global frame of segment 
        '''''
        super().extract_frames(left, right, upper, lower, frame_start, frame_end)
        frames_to_read = frame_end - frame_start +1 
        firs_pos = frame_start-self.g_l+self.i_l
        frames = np.load(self.file_name)
        frames = frames[firs_pos:firs_pos+frames_to_read]
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames

    def get_frame(self,value):
        frames = np.load(self.file_name)
        firs_pos = value-self.g_l+self.i_l
        frame = frames[firs_pos]
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return (frame,value)
        


class Videodata:

    def __init__(self):
        self.capturer = None
        self.fps = None
        self.frame_count = None
        self.frame_map = []

    def open_video(self, video):
        '''
        Set the video to work on
        :param video: Video path
        '''
        cap = cv.VideoCapture(video)
        self.capturer = cap
        self.fps = cap.get(cv.CAP_PROP_FPS)
        self.frame_count = cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH ))   # float `width`
        self.height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        interval = VideoInterval(0,self.frame_count,0,self.frame_count)
        self.frame_map.append(interval)

    def get_video_data(self):
        return (0, self.frame_count, self.width ,self.height)

    def get_frame(self,value):
        for node in self.frame_map:
            if node.g_l <= value<  node.g_r:
                return node.get_frame(value) 


    def get_frames():
        pass