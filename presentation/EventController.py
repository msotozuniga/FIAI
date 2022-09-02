from presentation.GUI import Mainwindow
from processing.VideoManager import VideoManager


class EventController():

    def __init__(self, manager, window) -> None:

        self.video_manager = manager
        self.window = window

    def execute_function(self, function, args, to_gui):
        if to_gui == 1:
            function(self.window, args)
        elif to_gui == -1:
            function(self.video_manager, args)
        else:
            function(self.window, self.video_manager, args)



    def run(self):
        while True:
            continue

    
        

    
