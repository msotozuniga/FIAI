# Usar el qt designer ubicado en C:\Users\Javier\Documents\Programas\project-env\Lib\site-packages\PySide2
import sys
from presentation.GUI import Mainwindow
from PySide2.QtWidgets import QApplication

if not QApplication.instance():
    app = QApplication(sys.argv)
else:
    app = QApplication.instance()
window = Mainwindow()
window.show()

app.exec_()