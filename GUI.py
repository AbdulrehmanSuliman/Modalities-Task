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

        self.coronalDisplay = ImageDisplay()
        self.layout_main.addWidget(self.coronalDisplay, 1, 1)

        self.axialdisplay = ImageDisplay()
        self.layout_main.addWidget(self.axialdisplay, 1, 0)

        self.sagitalDisplay = ImageDisplay()
        self.layout_main.addWidget(self.sagitalDisplay, 2, 0)

        self.obliqueDisplay = ImageDisplay()
        self.layout_main.addWidget(self.obliqueDisplay, 2, 1)

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
        self.axialdisplay.displayVolume(self.axialVolume)
        self.coronalDisplay.displayVolume(self.coronalVolume)
        self.sagitalDisplay.displayVolume(self.sagitalVolume)
        self.obliqueDisplay.displayVolume(self.axialVolume)

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
            for x in range(dicomVolume[i].shape[1]):
                sagitalVolume[x, :, i] = dicomVolume[i, :, x]
            for x in range(dicomVolume[i].shape[0]):
                coronalVolume[x, i, :] = dicomVolume[i, x, :]
        sagitalVolume = np.rot90(sagitalVolume, axes=(1, 0))
        coronalVolume = np.rot90(coronalVolume, axes=(1, 0))
        return (dicomVolume, sagitalVolume, coronalVolume)
