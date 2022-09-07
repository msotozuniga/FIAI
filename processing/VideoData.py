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
        self.cap.set(cv.CAP_PROP_POS_FRAMES,firs_pos)
        ret, frame = self.cap.read()
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
        return frame
        


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
        interval = VideoInterval(0,self.frame_count,0,self.frame_count,self.capturer)
        self.frame_map.append(interval)

    def get_video_data(self):
        return (0, self.frame_count, self.width ,self.height)

    def get_frame(self,value):
        for node in self.frame_map:
            if node.g_l <= value<  node.g_r:
                return node.get_frame(value)
        return (None,-1)


    def extract_frames(self, left,right,up,down, frame_start, frame_end):
        l = frame_start
        r = frame_end
        extracted_pieces =[]
        extracted_frames =[]
        for node in self.frame_map:
            l_check = node.g_l <= l <  node.g_r
            if l_check and r < node.g_r:
                pieces, frames = node.extract_frames(left, right, up, down, l, r)
                extracted_pieces.append(pieces)
                extracted_frames.append(frames)
                break
            elif l_check and node.g_r <= r:
                pieces, frames = node.extract_frames(left, right, up, down, l, node.g_r)
                extracted_pieces.append(pieces)
                extracted_frames.append(frames)
                l=node.g_r
            elif node.g_r <= l:
                continue
            else:
                raise NameError("Ocurrio un error en extractor: el borde izquierdo resulto menor que algun izquierdo global de un nono")
        todas_pieces = np.concatenate(extracted_pieces,axis=0)
        todas_frames = np.concatenate(extracted_frames,axis=0)
        return todas_pieces, todas_frames



