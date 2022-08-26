from processing.VideoManager import VideoManager
from presentation.GUI import Mainwindow


class EventListener:

    def __init__(self) -> None:

        self.video_manager = VideoManager
        self.window = Mainwindow()

    def execute_action(self,function, arguments):
        pass

    def run(self):
        while True:
            items = self.queue.get()
            func = items[0]
            args = items[1:]
            x = self.execute_action(self.something, *args)
            if x is True:
                break
