import presentation.GUI as GUI
import processing.VideoManager as VM

def closeProgram(window, manager, message):
    print("closing program with message " + message )
    manager.clear_cache()

def saveVideo(window,manager,message):
    manager.save_video(message)

def interpolate(window,manager, data):
    data = manager.interpolate(data)
    update_video_data = manager.get_video_data()
    window.setVideoData(update_video_data)
    responseFrame(window,data)


def openVideo(window, manager,file_name):
    manager.clear_cache()
    data = manager.open_video(file_name)
    window.setVideoData(data)
    requestFrame(window,manager,0)

def requestFrame(window, manager,value):
    data=manager.get_frame(value)
    window.setFrame(data)

def responseFrame(window, data):
    window.setFrame(data)