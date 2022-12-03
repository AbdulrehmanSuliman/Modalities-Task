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
        self.horizontalPressed = False
        self.verticalPressed = False
        return

    def mouse_press(self, event):
        print(event.xdata, event.ydata)
        if self.axialdisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.axialdisplay
        elif self.coronalDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.coronalDisplay
        elif self.sagitalDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.sagitalDisplay
        elif self.obliqueDisplay.ImageDisplayer.axes == event.inaxes:
            self.activeFigure = self.obliqueDisplay
        x, y = event.xdata, event.ydata

        if y <= self.activeFigure.horizontalLine.get_ydata()+10 and y >= self.activeFigure.horizontalLine.get_ydata()-10:
            self.horizontalPressed = True

        if x <= self.activeFigure.verticalLine.get_xdata()+10 and x >= self.activeFigure.verticalLine.get_xdata()-10:
            self.verticalPressed = True

        #--------------------TODO--------------------#
        # getting data of oblique line
        x, y = self.activeFigure.obliqueLine.get_data()
        # setting data of oblique line
        # p1 = [0,0] and p2 = [0.5,0.9]
        self.activeFigure.obliqueLine.set_data([0, 0.5], [0, 0.9])

        # to show results you must draw and update
        # self.activeFigure.ImageDisplayer.figure.canvas.draw()
        # self.activeFigure.update()

    def mouse_move(self, event):
        if not(self.verticalPressed or self.horizontalPressed):
            return
        if self.horizontalPressed:
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
