import queue
import threading
import settings
import time
from presentation.GUI import Mainwindow
from processing.VideoManager import VideoManager
from PySide2.QtWidgets import QApplication


class EventController():

    def __init__(self, manager=None, window=None) -> None:

        self.video_manager = manager
        self.window = window

    def setManager(self, video_manager):
        self.video_manager = video_manager

    def setWindow(self, window):
        self.window = window

    def executeFunction(self, function, args, to_gui):
        if to_gui >0:
            function(self.window, args)
        elif to_gui < 0:
            function(self.video_manager, args)
        else:
            function(self.window, self.video_manager, args)



    def run(self):
        while True:
            func, params, to_gui = settings.process_queue.get()
            self.executeFunction(func,params,to_gui)
        

        

    
        

    
