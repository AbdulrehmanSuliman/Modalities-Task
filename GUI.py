from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont, QIcon
from Helpers import BrowseWidget
import pydicom as dicom
from ImageDisplayerMatplot import ImageDisplay
import numpy as np
import os
TEXT_COLOR = "color: #BCBCBC;"

PUSH_BUTTON_STYLE = """QPushButton {
    color: #BCBCBC;
    background: #0F62FE;
    border-width: 0px;
    border-color: yellow;
    border-style: solid;
    border-radius: 10px;
    min-width: 3em;
    min-height: 30px;
    padding: 6px;}
    
    QPushButton:hover {
background-color: #c2c2c2;
color: black;
}
    QPushButton:pressed {
background-color: #FFFFFF;
color: black;
}
"""


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")
        self.main_widget = QtWidgets.QWidget(self)
        self.layout_main = QtWidgets.QGridLayout(self.main_widget)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        self.browse = BrowseWidget()
        self.browse.browse_button.clicked.connect(lambda: self.BrowseClicked())
        self.layout_main.addWidget(self.browse, 0, 0, 1, 2)

        self.coronalDisplay = ImageDisplay("coronal")
        self.layout_main.addWidget(self.coronalDisplay, 1, 1)

        self.axialdisplay = ImageDisplay("axial")
        self.layout_main.addWidget(self.axialdisplay, 1, 0)

        self.sagitalDisplay = ImageDisplay("sagital")
        self.layout_main.addWidget(self.sagitalDisplay, 2, 0)

        self.obliqueDisplay = ImageDisplay("oblique")
        self.layout_main.addWidget(self.obliqueDisplay, 2, 1)

        self.horizontalPressed = False
        self.verticalPressed = False
        self.obliqueAnglePressed = False
        self.obliquePressed = False
        self.slope = 1
        self.bias = 0
        self.x1 = 0
        self.y1 = 0

        self.activeFigure = None

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.resize(1080, 720)

    def BrowseClicked(self):
        """saves the image from path and creates the image info string
        """
        ImagesPath = self.open_dialog_box()

        self.browse.browse_text.insert(ImagesPath)

        self.axialVolume, self.sagitalVolume, self.coronalVolume,  = self.create3DMatrix(
            ImagesPath)
        self.axialdisplay.displayVolume(
            self.axialVolume, int(self.axialVolume.shape[0]/2))
        self.axialdisplay.createLines(
            self.mouse_press, self.mouse_move, self.mouse_release)
        self.coronalDisplay.displayVolume(
            self.coronalVolume, int(self.coronalVolume.shape[0]/2))
        self.coronalDisplay.createLines(
            self.mouse_press, self.mouse_move, self.mouse_release)
        self.sagitalDisplay.displayVolume(
            self.sagitalVolume, int(self.sagitalVolume.shape[0]/2))
        self.sagitalDisplay.createLines(
            self.mouse_press, self.mouse_move, self.mouse_release)
        self.obliqueDisplay.displayVolume(
            self.axialVolume, int(self.axialVolume.shape[0]/2))

    def open_dialog_box(self):
        """Creates a diaglog box for the user to select file and check if it's an image

        Returns:
            [str, str]: array of the filepath path and file type
        """
        filename = str(QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory"))
        return filename

    def create3DMatrix(self, path):

        # counting the slices in the passed folder
        files = os.listdir(path)
        file_count = len(files)
        # calculate the aspect ratio
        slices = [dicom.read_file(path+'/'+s, force=True) for s in files]
        pixel_spacing = slices[0].PixelSpacing
        slices_thickess = slices[0].SliceThickness

        axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
        sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
        coronal_aspect_ratio = slices_thickess/pixel_spacing[0]

        print("Axial Aspect Ratio:", axial_aspect_ratio)
        print("Sagital Aspect Ratio:", sagital_aspect_ratio)
        print("Coronal Aspect Ratio:", coronal_aspect_ratio)
        # creating an initial dicom reader of the first frame
        ds = dicom.dcmread(path + '/' + files[0])

        # using the initial dicom reader object,
        # we created a 3D Matrix with length and width of the inital object
        # and depth of the same number of files in the passed path.
        # 3 volumes are created for each view, e.g. axial, corornal, sagital
        dicomVolume = np.zeros(
            (file_count, ds.pixel_array.shape[0], ds.pixel_array.shape[1]))
        sagitalVolume = np.zeros(
            (ds.pixel_array.shape[0], ds.pixel_array.shape[1], file_count)
        )
        coronalVolume = np.zeros(
            (ds.pixel_array.shape[1], file_count, ds.pixel_array.shape[0])
        )

        # setting the data of each volume
        for i in range(file_count):
            dicomVolume[i] = dicom.dcmread(path + '/' + files[i]).pixel_array
        sagitalVolume = np.rot90(
            np.rot90(dicomVolume, axes=(0, 2)), axes=(1, 2))
        coronalVolume = np.rot90(dicomVolume, axes=(1, 0))
        return (dicomVolume, sagitalVolume, coronalVolume)

    def mouse_release(self, event):
        if self.obliqueAnglePressed or self.obliquePressed:
            print("oblique line")
        self.horizontalPressed = False
        self.verticalPressed = False
        self.obliqueAnglePressed = False
        self.obliquePressed = False

        return

    def mouse_press(self, event):
        if self.axialdisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.axialdisplay
        elif self.coronalDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.coronalDisplay
        elif self.sagitalDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.sagitalDisplay
        elif self.obliqueDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.obliqueDisplay
        x, y = event.xdata, event.ydata
        # Check if the click is on the horizonal line or not
        # and with 10 pixels magin of error
        if y <= self.activeFigure.horizontalLine.get_ydata()+10 and y >= self.activeFigure.horizontalLine.get_ydata()-10:
            self.horizontalPressed = True

        # Check if the click is on the vertical line or not
        # and with 10 pixels magin of error
        if x <= self.activeFigure.verticalLine.get_xdata()+10 and x >= self.activeFigure.verticalLine.get_xdata()-10:
            self.verticalPressed = True
        # oblique only exists on the axial display
        if self.activeFigure.displayType == "axial":
            # Check if the click is on the oblique line (Check if the points satisfy the equation of line)
            if y <= self.slope * x + self.bias + 10 and y >= self.slope * x + self.bias - 10:
                # To determine what to do (drag or rotate) check if the click is at the end if the canvas in
                # x or y direction, in other words, we click at the edge of the line to rotate and else where to drag
                if (int(self.axialVolume.shape[1]) - int(event.xdata) <= 13) or (int(self.axialVolume.shape[1]) - int(event.ydata) <= 13):
                    self.obliqueAnglePressed = True
                else:
                    self.obliquePressed = True

    def mouse_move(self, event):
        if not(self.verticalPressed or self.horizontalPressed or self.obliqueAnglePressed or self.obliquePressed):
            return
        if self.obliqueAnglePressed:
            # The angle needs to be changed based on two points
            if event.xdata != None and event.ydata != None:
                self.activeFigure.obliqueLine.remove()
                # Draw the new line based on the two points
                self.activeFigure.obliqueLine = self.activeFigure.ImageDisplayer.axes.axline(
                    (self.x1, self.y1), (event.xdata, event.ydata))
                self.slope = (event.ydata-self.bias)/event.xdata

        if self.obliquePressed:
            # get the new bias and get the first point at which the line
            # intersects with the x or y axis
            x1 = event.xdata
            y1 = event.ydata
            self.bias = y1 - self.slope * x1
            x2 = 0
            y2 = self.slope*x2 + self.bias
            if y2 < 0:
                # The y point is negative so the line intersects the positive x axis
                y2 = 0
                x2 = (y2-self.bias)/self.slope
            self.x1 = x2
            self.y1 = y2
            self.activeFigure.obliqueLine.remove()
            # Draw the new line based on the point and the slope
            self.activeFigure.obliqueLine = self.activeFigure.ImageDisplayer.axes.axline(
                (x1, y1), slope=self.slope)

        if self.horizontalPressed:
            # The horizontal line is pressed so set the ydata of the point clicked to the line
            # and send the value to the coresponding plane viewer to get the corresponding slice on the other plane
            self.activeFigure.horizontalLine.set_ydata(event.ydata)
            if self.activeFigure.displayType == "axial":
                self.coronalDisplay.displayVolume(
                    self.coronalVolume, int(event.ydata))
            elif self.activeFigure.displayType == "coronal":
                self.axialdisplay.displayVolume(
                    self.axialVolume, int(event.ydata))
            elif self.activeFigure.displayType == "sagital":
                self.axialdisplay.displayVolume(
                    self.axialVolume, int(event.ydata))

        if self.verticalPressed:
            # The vertical line is pressed so set the xdata of the point clicked to the line
            # and send the value to the coresponding plane viewer to get the corresponding slice on the other plane
            self.activeFigure.verticalLine.set_xdata(event.xdata)
            if self.activeFigure.displayType == "axial":
                self.sagitalDisplay.displayVolume(
                    self.sagitalVolume, int(event.xdata))
            elif self.activeFigure.displayType == "coronal":
                self.sagitalDisplay.displayVolume(
                    self.sagitalVolume, int(event.xdata))
            elif self.activeFigure.displayType == "sagital":
                self.coronalDisplay.displayVolume(
                    self.coronalVolume, int(event.xdata))

        self.activeFigure.ImageDisplayer.figure.canvas.draw()
        self.activeFigure.update()
