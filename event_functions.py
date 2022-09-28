import presentation.GUI as GUI
import processing.VideoManager as VM

def closeProgram(window, manager, message):
    print("closing program with message " + message )
    manager.clearCache()

def saveVideo(window,manager,message):
    manager.saveVideo(message)

def interpolate(window,manager, data):
    data = manager.interpolate(data)
    update_video_data = manager.getVideoData()
    window.setVideoData(update_video_data)
    responseFrame(window,data)


def openVideo(window, manager,file_name):
    manager.clearCache()
    data = manager.openVideo(file_name)
    window.setVideoData(data)
    requestFrame(window,manager,0)

def requestFrame(window, manager,value):
    data=manager.getFrame(value)
    window.setFrame(data)

def responseFrame(window, data):
    window.setFrame(data)

def deleteFrame(window,manager,value):
    data = manager.deleteFrame(value)
    update_video_data = manager.getVideoData()
    window.setVideoData(update_video_data)
    responseFrame(window,data)