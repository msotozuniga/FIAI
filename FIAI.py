import sys
from processing.VideoManager import VideoManager
import settings
from presentation.GUI import Mainwindow
from PySide2.QtWidgets import QApplication


settings.initialize_queue()
if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
window = Mainwindow()
manager = VideoManager()

window.show()

app.exec_()

# Usar el qt designer ubicado en C:\Users\Javier\Documents\Programas\project-env\Lib\site-packages\PySide2

'''
import threading
import queue
import time





def print_function(something,message):
    print(message+something)


def close(something, message):
    print("closing with message "+message)
    return True

class A:
    def __init__(self, queue) -> None:
        self.information = "this is class A"
        self.queue = queue

    def send_singal(self):
        self.queue.put((print_function, self.information))

class B:
    def __init__(self, queue) -> None:
        self.information = "this is class B"
        self.queue = queue

    def send_singal(self):
        self.queue.put((print_function, self.information))

class test:

    def __init__(self) -> None:
        self.something = "Something"
        self.queue = queue.Queue()
        self.a = A(self.queue)
        self.b=B(self.queue)
    

    def run(self):
        while True:
            try:
                items = self.queue.get()
                func = items[0]
                args = items[1:]
                x = func(self.something, *args)
                if x is True:
                    break
                
            except:
                print("NO execution")
            finally:
                print("loop")
        

testing_threads = test()
t = threading.Thread(target=testing_threads.run)
t.start()
time.sleep( 1 )
testing_threads.a.send_singal()
time.sleep( 2)
testing_threads.b.send_singal()
time.sleep( 1 )
testing_threads.queue.put( (close,"data") )
time.sleep( 1 )
t.join()

'''