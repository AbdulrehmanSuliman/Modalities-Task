from time import sleep
from cv2 import repeat
from matplotlib import animation
from matplotlib.pyplot import draw
import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
import os


def create3DMatrix(path):

    #counting the slices in the passed folder
    files = os.listdir(path)
    file_count = len(files)
    #calculate the aspect ratio
    slices = [dicom.read_file(path+'/'+s,force=True) for s in files]
    pixel_spacing = slices[0].PixelSpacing
    slices_thickess = slices[0].SliceThickness

    axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
    sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
    coronal_aspect_ratio = slices_thickess/pixel_spacing[0]

    #print("Pixel spacing is:",pixel_spacing)
    #print("Slices Thickness is:",slices_thickess)
    print("Axial Aspect Ratio:",axial_aspect_ratio)
    print("Sagital Aspect Ratio:",sagital_aspect_ratio)
    print("Coronal Aspect Ratio:",coronal_aspect_ratio)
    #creating an initial dicom reader of the first frame 
    ds = dicom.dcmread(path+files[0])

    #using the initial dicom reader object,
    # we created a 3D Matrix with length and width of the inital object
    # and depth of the same number of files in the passed path.
    # 3 volumes are created for each view, e.g. axial, corornal, sagital 
    dicomVolume = np.zeros(
        (file_count, ds.pixel_array.shape[0], ds.pixel_array.shape[1]))
    sagitalVolume = np.zeros(
        (ds.pixel_array.shape[0],ds.pixel_array.shape[1],file_count)
    )
    coronalVolume = np.zeros(
        (ds.pixel_array.shape[1],file_count,ds.pixel_array.shape[0])
    )

    # setting the data of each volume
    for i in range(file_count):
        dicomVolume[i] = dicom.dcmread(path+files[i]).pixel_array
        for x in range(dicomVolume[i].shape[1]):
            sagitalVolume[x,:,i] = dicomVolume[i,:,x]
        for x in range(dicomVolume[i].shape[0]):
            coronalVolume[x,i,:] = dicomVolume[i,x,:]

    return (dicomVolume, sagitalVolume, coronalVolume)


def navigateSlices(axialVolume, sagitalVolume=0, coronalVolume=0):
    #variable that decides the time per frame in milliseconds
    interval = 0.3

    #getting the maximum number of frames 
    frames = len(axialVolume)
    if frames <= len(sagitalVolume):
        frames = len(sagitalVolume)
    if frames <= len(coronalVolume):
        frames = len(coronalVolume)

    #creating an initial frame to hold the imshow object for each volume
    fig, axesPlot = plt.subplots(2,2)
    imshowObjAx = axesPlot[0,0].imshow(axialVolume[230], cmap='gray')
    axesPlot[0,0].axis('off')
    axesPlot[0,0].title.set_text('Axial')

    imshowObjSag = axesPlot[0,1].imshow(sagitalVolume[230], cmap='gray')
    axesPlot[0,1].axis('off')
    axesPlot[0,1].title.set_text('Sagital')
    
    imshowObjCor = axesPlot[1,0].imshow(coronalVolume[230], cmap='gray')
    axesPlot[1,0].axis('off')
    axesPlot[1,0].title.set_text('Coronal')
    axesPlot[1,1].axis('off')


    #function that takes a specific frame and updates all imshow objects
    def animate(i):
        if i<len(axialVolume):
            imshowObjAx.set_data(axialVolume[i])
        if i<len(sagitalVolume):
            imshowObjSag.set_data(sagitalVolume[i])
        if i<len(coronalVolume):
            imshowObjCor.set_data(coronalVolume[i])

    #using matplotlib animfunction to display the slices smoothly
    anim = animation.FuncAnimation(
        fig, animate, frames=frames, interval=interval, repeat=False)

    #Removes the toolbar from matplotlib window
    plt.rcParams['toolbar'] = 'None'


    plt.show()


volume, volume1, volume2 = create3DMatrix('Head/')
navigateSlices(volume,volume1,volume2)