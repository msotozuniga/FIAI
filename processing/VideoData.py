from xml.dom.minidom import Element
import cv2 as cv
import numpy as np
import os
import uuid
import pickle


class Frame:

    def __init__(self, internal_frame,type):
        self.i_frame = internal_frame
        self.type = type

    def equal(self,obj):
        return type(self) is type(obj)

class VideoFrame(Frame):

    def __init__(self, internal_frame):
        super().__init__(internal_frame, 0)

    def get_frame(self,cap):
        cap.set(cv.CAP_PROP_POS_FRAMES,self.i_frame)
        ret, frame = cap.read()
        if not ret:
            return (None,-1)
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return frame

    @staticmethod
    def extract_frames(left, right, upper, lower, frame_start, frame_end,cap):
        if frame_start ==None or frame_end ==None:
            return None,None, True
        frames_to_read = frame_end - frame_start +1 
        frames = []
        cap.set(cv.CAP_PROP_POS_FRAMES,frame_start)
        for i in range(frames_to_read):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        frames = np.stack(frames)
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames, False
        

class StubFrame(Frame):

    def __init__(self, internal_frame, filename):
        super().__init__(internal_frame, 1)
        self.file_name = filename

    def get_frame(self):
        frames = np.load(self.file_name)
        frame = frames[self.i_frame]
        cv.cvtColor(frame,cv.COLOR_BGR2RGB, frame)
        return frame


    def equal(self, obj):
        temp =  super().equal(obj)
        if temp:
            return self.file_name ==obj.file_name
        return temp

    @staticmethod
    def extract_frames(left, right, upper, lower, frame_start, frame_end,file_name):
        if frame_start ==None or frame_end ==None:
            return None,None, True
        frames = np.load(file_name)
        frames = frames[frame_start:frame_end+1]
        pieces = frames[:, upper:lower,left:right]
        return pieces, frames, False

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
        frame_map = []
        for frame_id in range(int(self.frame_count)):
            frame_map.append(VideoFrame(frame_id))
        self.dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"temp")
        if not os.path.exists(self.dir_path):
            os.makedirs(self.dir_path)
        self.map_path = os.path.join(self.dir_path,"map.bn")
        self.path_temp = os.path.join(self.dir_path,"temp.npy")
        self.frame_map = frame_map

    def get_video_data(self):
        return (0, self.frame_count, self.width ,self.height)

    def get_frame(self,value):
        try:
            frame= self.frame_map[value]
        except:
            return None, -1
        if type(frame) is VideoFrame:
            data = frame.get_frame(self.capturer)
        else:
            data = frame.get_frame()
        return data, value

    def delete_frame(self,value):
        self.frame_map.pop(value)

    def save_map(self):
        with open(self.map_path, "wb") as fp:   #Pickling
            pickle.dump(self.frame_map, fp)
        self.frame_map = None

    def load_map(self):
        with open(self.map_path, "rb") as fp:   #Pickling
            self.frame_map = pickle.load(fp)


    

    def stitch(self, pieces, left, right, lower, upper, n_frames):
        '''
        Pieces: (n,h,w,c)
        '''
        frames = np.load(self.path_temp) #usar repear en dim 0 para llegar al limite
        frames = np.repeat(frames,n_frames+1,axis=0)[:-1*(n_frames+1)]
        frames[:, upper:lower, left:right] = pieces
        if os.path.isfile(self.path_temp):
            os.remove(self.path_temp)
        return frames


    def extract_frames(self, left,right,up,down, frame_start, frame_end):
        #TODO: agarrar el tipo del primer frame
        curr_obj = self.frame_map[frame_start]
        curr_type = type(curr_obj)
        curr_add_on = curr_obj.file_name if curr_type is StubFrame else self.capturer
        curr_interval = [curr_obj.i_frame,None]
        frames_sets =[]
        pieces_sets = []
        for i in range(frame_start,frame_end+1):
            element = self.frame_map[i]
            if not element.equal(curr_obj):
                piece,frame, empty =curr_type.extract_frames(left, right, up, down, curr_interval[0],curr_interval[1],curr_add_on)
                if not empty:
                    pieces_sets.append(piece)
                    frames_sets.append(frame)
                curr_type = type(element)
                curr_obj = element
                curr_add_on = element.file_name if curr_type is StubFrame else self.capturer
                curr_interval[0] = element.i_frame
            curr_interval[1]=element.i_frame
        piece,frame, empty =curr_type.extract_frames(left, right, up, down, curr_interval[0],curr_interval[1],curr_add_on) 
        if not empty:
            pieces_sets.append(piece)
            frames_sets.append(frame)  
        todas_pieces = np.concatenate(pieces_sets[:],axis=0)
        todas_frames = np.concatenate(pieces_sets[:],axis=0)
        return todas_pieces,todas_frames

    def insert_frames(self, stub_name,frames_added, l,r):
        for i in range(r-l):
            self.frame_map.pop(l)
        index = l
        for i in range(frames_added):
            stub_frame = StubFrame(i,stub_name)
            self.frame_map.insert(index,stub_frame)
            index +=1

    def add_frames(self, result, frame_start,frame_end):
        frames_added,_,_,_ = result.shape
        file_id = uuid.uuid4().hex[:10].upper() + ".npy"
        stub_path = os.path.join(self.dir_path,file_id)
        self.save_frames(stub_path,result)
        self.insert_frames(stub_path,frames_added,frame_start,frame_end)
        self.frame_count = self.frame_count + frames_added - (frame_end-frame_start)
        return result[1], frame_start+1

    @staticmethod
    def save_frames(path, frames):
        np.save(path, frames)
        




