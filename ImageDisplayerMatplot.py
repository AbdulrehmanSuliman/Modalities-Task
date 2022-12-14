from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse


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
        self.tempPoint = None
        self.tempPoint2 = None
        self.tempPoint3 = None
        self.Measurments = {
            "line": [],
            "angle": [],
            "polygon": [],
            "ellipse": [],
        }

        self.setLayout(self.layout_main)
        self.MessageBox = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Warning, "Error", "Error")

    def displayVolume(self, volume, slice=None):
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

    def deleteLines(self):
        self.horizontalLine.remove()
        self.verticalLine.remove()
        if self.displayType == "axial":
            self.obliqueLine.remove()
        # self.ImageDisplayer.draw()
        self.ImageDisplayer.figure.canvas.draw()
        self.update()

    def addEllipseMeasurements(self, point, hasReleased):
        if self.tempPoint == None:
            self.tempPoint = point
            self.tempEllipse = Ellipse(point, 0, 0)
            self.tempEllipse.set(fill=False, linewidth=2, color='yellow')
            self.ImageDisplayer.axes.add_patch(self.tempEllipse)
            return

        self.tempEllipse.set_width(2*abs(self.tempPoint[0]-point[0]))
        self.tempEllipse.set_height(2*abs(self.tempPoint[1]-point[1]))
        if hasReleased:
            self.Measurments['ellipse'].append((self.tempEllipse.width, self.tempEllipse.height))
            # self.Measurments['ellipse'].append((self.tempPoint, point))
            # print(self.tempEllipse.width)
            # print(self.tempEllipse.height)
            self.tempPoint = None
        self.ImageDisplayer.figure.canvas.draw()
        self.update()

    def addPolygonMeasurements(self, point):
        if self.tempPoint == None:
            self.tempPoint = point
            return
        if self.tempPoint2 == None:
            self.tempPoint2 = point
            self.ImageDisplayer.axes.plot(
                [self.tempPoint[0], self.tempPoint2[0]], [self.tempPoint[1], self.tempPoint2[1]], 'k-', color='blue', linewidth=2)
            self.ImageDisplayer.figure.canvas.draw()
            self.update()
            return
        if self.tempPoint3 == None:
            self.tempPoint3 = point
            self.ImageDisplayer.axes.plot(
                [self.tempPoint2[0], self.tempPoint3[0]], [self.tempPoint2[1], self.tempPoint3[1]], 'k-', color='blue', linewidth=2)
            self.ImageDisplayer.figure.canvas.draw()
            self.update()
            return
        self.ImageDisplayer.axes.plot(
            [self.tempPoint3[0], point[0]], [self.tempPoint3[1], point[1]], 'k-', color='blue', linewidth=2)
        self.ImageDisplayer.axes.plot(
            [self.tempPoint[0], point[0]], [self.tempPoint[1], point[1]], 'k-', color='blue', linewidth=2)
        self.Measurments["polygon"].append(
            (self.tempPoint, self.tempPoint2, self.tempPoint3, point))
        self.tempPoint = None
        self.tempPoint2 = None
        self.tempPoint3 = None
        self.ImageDisplayer.figure.canvas.draw()
        self.update()

    def addAngleMeasurements(self, point):
        if self.tempPoint == None:
            self.tempPoint = point
            return
        if self.tempPoint2 == None:
            self.tempPoint2 = point
            self.ImageDisplayer.axes.plot(
                [self.tempPoint[0], self.tempPoint2[0]], [self.tempPoint[1], self.tempPoint2[1]], 'k-', color='red', linewidth=2)
            self.ImageDisplayer.figure.canvas.draw()
            self.update()
            return

        self.ImageDisplayer.axes.plot(
            [self.tempPoint2[0], point[0]], [self.tempPoint2[1], point[1]], 'k-', color='red', linewidth=2)
        self.Measurments["angle"].append(
            (self.tempPoint, self.tempPoint2, point))
        self.tempPoint = None
        self.tempPoint2 = None
        self.ImageDisplayer.figure.canvas.draw()
        self.update()

    def addLineMeasurements(self, point):
        if self.tempPoint == None:
            self.tempPoint = point
            return
        else:
            self.ImageDisplayer.axes.plot(
                [self.tempPoint[0], point[0]], [self.tempPoint[1], point[1]], 'k-', color='green', linewidth=2)
            self.Measurments["line"].append((point, self.tempPoint))
            self.tempPoint = None

            self.ImageDisplayer.figure.canvas.draw()
            self.update()

    def enableMeasurments(self, mouse_press, mouse_move, mouse_release):
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'button_press_event', mouse_press)
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'button_release_event', mouse_release)
        self.ImageDisplayer.figure.canvas.mpl_connect(
            'motion_notify_event', mouse_move)

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

        self.ImageDisplayer.figure.canvas.draw()
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
