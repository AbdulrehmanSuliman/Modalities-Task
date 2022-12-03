from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.figure = Figure(figsize=(width, height),
                             dpi=dpi, facecolor='#1e1e1e')
        self.axes = self.figure.add_subplot(111)
        self.figure.subplots_adjust(bottom=0, top=1, left=0, right=1)
        self.axes.axis('off')
        super(MplCanvas, self).__init__(self.figure)


class ImageDisplay(QtWidgets.QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ImageDisplayer = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout_main = QtWidgets.QGridLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.addWidget(self.ImageDisplayer)
        self.canvasWidth = 700
        self.canvasHeight = 300
        self.setLayout(self.layout_main)
        self.MessageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Warning, "Error", "Error")

    def displayVolume(self, volume):
        """Sets the path of the image and generates the information and puts it in a dictionary called Info

        Args:
            path (str): File Path
        """
        self.ImageDisplayer.axes.imshow(volume[233], cmap='gray')
        self.horizontalLine = self.ImageDisplayer.axes.axhline(y=50)
        self.verticalLine = self.ImageDisplayer.axes.axvline(x=50)
        self.horizontalLine.set_visible(True)
        self.verticalLine.set_visible(True)
        self.ImageDisplayer.figure.canvas.mpl_connect('motion_notify_event', self.onMouseMove)



        self.setFixedWidth(self.canvasWidth)
        self.setFixedHeight(self.canvasHeight)
        self.update()

    def DisplayError(self, title, Message):
        """Creates a messsage box when and error happens

        Args:
            title (str): title of the error message
            Message (str): information about the error to be displayed
        """
        self.MessageBox.setWindowTitle(title)
        self.MessageBox.setText(Message)
        self.MessageBox.exec()

    def onMouseMove(self, event):
        x,y = event.xdata, event.ydata
        print('x: {}, y: {}'.format(x,y))
        print(y)
        self.horizontalLine.set_ydata(y)
        self.verticalLine.set_xdata(x)
        self.ImageDisplayer.figure.canvas.draw()
        self.update()