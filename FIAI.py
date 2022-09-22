import sys

import settings
import threading
from presentation.GUI import Mainwindow
from processing.VideoManager import VideoManager
from presentation.EventController import EventController
from PySide2.QtWidgets import QApplication


settings.initializeQueue()


if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()

    
window = Mainwindow()
manager = VideoManager()
controller = EventController(manager,window)
controller_thread = threading.Thread(target=controller.run)
controller_thread.setDaemon(True)
controller_thread.start()
window.show()

app.exec_()



