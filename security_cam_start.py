
# External Library Imports
from picamera import PiCamera
# Internal Library Imports
from lib import fuzzy_clustering as fcm

from time import sleep
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import skfuzzy as fuzz

# Camera Parametesr and Initialization
print("Intialization Camera")
camera = PiCamera()
camera.rotation = 0
img_width = 320
img_height = 240
camera.resolution = (img_width, img_height)

for i in range(5):
    print("Taking Image Number: %s" % i)
    sleep(1)
    # camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    im = Image.fromarray(output)
    print("Saving Original Image")
    im.save('./outputImages/%s_OriginalImage.jpg' % i)

    fcm.fuzzyClusteringOnImage(output)

    colors = ['black', 'orange', 'grey']

    # Define three cluster centers and parameters
    centers = [[0, 0, 0],
               [122, 122, 122],
               [255, 255, 255]]
    numClusters = 3
    maxIter = 100

    redPixelValues = output[:, :, 0].flatten()
    greenPixelValues = output[:, :, 1].flatten()
    bluePixelValues = output[:, :, 2].flatten()
    mydata = np.vstack((redPixelValues, greenPixelValues, bluePixelValues))
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        mydata, c=numClusters, m=2, error=0.005, maxiter=1000)

    numPixels = len(u[0, :])
    pixelClassification = np.empty(numPixels)
    for j in range(0, numPixels):
        pixelClassification[j] = u[:, j].argmax()

    pixelClassifiedImage = pixelClassification.reshape(img_height, img_width)

    print("Saving Segmented Image")
    imgName = './outputImages/%s_ClusteredImage.jpg' % i
    plt.imsave(imgName, pixelClassifiedImage)
