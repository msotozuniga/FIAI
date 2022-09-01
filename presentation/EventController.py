from multiprocessing import Event
from processing.VideoManager import VideoManager
from presentation.GUI import Mainwindow



class EventController():

    def __init__(self, manager: VideoManager, window: Mainwindow) -> None:

        self.video_manager = manager
        self.video_manager.setController(self)
        self.window = window
        self.window.setController(self)

    def closeProgram(self):
        print("Closing program")

    def saveVideo(self):
        print("Saving video")

    def interpolateFrames(self, data: dict):
        print("interpolating")

    def changeFrame(self, value):
        print("changing value")

    def openVideo(self, file_name):
        print("Opening video")
        

    
