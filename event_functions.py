import queue
import presentation.GUI as GUI
import processing.VideoManager as VM


def initialize_queue():
    global process_queue
    process_queue = queue.Queue()

def closeProgram(window, manager):
    return
'''
    def saveVideo(self):
        print("Saving video")

    def interpolateFrames(self, data: dict):
        print("interpolating")

    def changeFrame(self, value):
        print("changing value")

    def openVideo(self, file_name):
        print("Opening video")
'''