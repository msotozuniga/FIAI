import queue

def initializeQueue():
    global process_queue
    global model_index
    global device_index
    model_index = {
        "RIFE": 0,
        "Softsplat": 1,
        "BLURIFE": 2
    }
    device_index = {
        "CPU":"cpu",
        "GPU":"cuda"
    }
    process_queue = queue.Queue()

