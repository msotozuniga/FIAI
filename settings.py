import queue
import threading



def initialize_queue():
    global process_queue
    global queue_condition
    queue_condition = threading.Condition()
    process_queue = queue.Queue()


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