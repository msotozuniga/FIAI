import queue
import threading



def initialize_queue():
    global process_queue
    global model_index
    global device_index
    model_index = {
        "RIFE": 0,
        "Softsplat": 1,
        "BLURIFE": 2
    }
    device_index = {
        "CPU":0,
        "GPU":1
    }
    process_queue = queue.Queue()
