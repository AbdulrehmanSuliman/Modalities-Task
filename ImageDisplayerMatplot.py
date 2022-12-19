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
    def __init__(self, sliceType):
        QWidget.__init__(self)
        self.ImageDisplayer = MplCanvas(self, width=5, height=4, dpi=100)
        self.layout_main = QtWidgets.QGridLayout()
        self.layout_main.setContentsMargins(0, 0, 0, 0)
        self.layout_main.addWidget(self.ImageDisplayer)
        self.canvasWidth = 700
        self.canvasHeight = 300
        self.displayType = sliceType
        self.obliqueLine = None

        self.setLayout(self.layout_main)
        self.MessageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Warning, "Error", "Error")

    def displayVolume(self, volume, slice = None):
        """Sets the path of the image and generates the information and puts it in a dictionary called Info

        Args:
            path (str): File Path
        """
        if slice == None:
            self.ImageDisplayer.axes.imshow(
                volume, cmap='gray')
        else:
            self.slice1 = int(volume.shape[1]/2)
            self.slice2 = int(volume.shape[2]/2)
            self.ImageDisplayer.axes.imshow(
                volume[slice], cmap='gray')

        self.setFixedWidth(self.canvasWidth)
        self.setFixedHeight(self.canvasHeight)

        if self.canvasWidth == 700:
            self.canvasWidth = 701
        else:
            self.canvasWidth = 700
        if self.canvasHeight == 300:
            self.canvasHeight = 301
        else:
            self.canvasHeight = 300

        self.update()

    def createLines(self, mouse_press, mouse_move, mouse_release):
        # create the lines horizontal, vertical, and oblique
        self.horizontalLine = self.ImageDisplayer.axes.axhline()
        self.horizontalLine.set_ydata(self.slice1)
        self.verticalLine = self.ImageDisplayer.axes.axvline()
        self.verticalLine.set_xdata(self.slice2)
        if self.displayType == "axial":
            self.obliqueLine = self.ImageDisplayer.axes.axline(
                (0, 0), slope=1)
            self.obliqueLine.set_data([0, 1], [0, 1])
            self.obliqueLine.set_visible(True)
        self.horizontalLine.set_visible(True)
        self.verticalLine.set_visible(True)
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'button_press_event', mouse_press)
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'button_release_event', mouse_release)
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'motion_notify_event', mouse_move)

    def DisplayError(self, title, Message):
        """Creates a messsage box when and error happens

        Args:
            title (str): title of the error message
            Message (str): information about the error to be displayed
        """
        self.MessageBox.setWindowTitle(title)
        self.MessageBox.setText(Message)
        self.MessageBox.exec()
