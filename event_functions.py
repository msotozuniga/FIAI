import presentation.GUI as GUI
import processing.VideoManager as VM

def closeProgram(window, manager, message):
    print("closing program with message " + message )
    manager.clear_cache()
    return

def saveVideo(window,manager,message):
    manager.save_video()
    return

def interpolate(manager, data):
    manager.interpolate(data)

def openVideo(manager,file_name):
    manager.open_video(file_name)
    manager.get_frame(0)

def requestFrame(manager,value):
    manager.get_frame(value)

def responseFrame(window, frame):
    print(frame)
    #window.showFrame(frame)