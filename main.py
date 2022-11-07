from __future__ import unicode_literals
import sys
from GUI import ApplicationWindow
from PyQt5.QtWidgets import QApplication

qApp = QApplication(sys.argv)
aw = ApplicationWindow()
aw.setWindowTitle("Image Viewer")
aw.show()
sys.exit(qApp.exec_())