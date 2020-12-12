
# External Library Imports
from picamera import PiCamera
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# Internal Library Imports
from lib import fuzzy_clustering as fcm
from lib import centroid_calculator as cc


def capturePic(cam):
    ret = 0
    image = 0
    for i in range(0, 10):
        ret, image = cam.read()
    return ret, image


    # Camera Parametesr and Initialization
print("Intialization Camera")
cam = cv2.VideoCapture(1)
img_width = 320
img_height = 240
cam.set(3, img_width)
cam.set(4, img_height)

for i in range(5):
    print("Taking Image Number: %s" % i)
    ret, imgArray = capturePic(cam)

    print("Saving Original Image")
    decodedImg = Image.fromarray(imgArray)
    decodedImg.save('./outputImages/%s_OriginalImage.jpg' % i)

    print("Performing fuzzy c means")
    clusteredImg, brightestClustIDs = fcm.fuzzyClusteringOnImage(
        imgArray, [img_width, img_height])

    colorMap = fcm.createColorMap(brightestClustIDs)

    x, y = cc.findBrightClusterCenter(
        clusteredImg, brightestClustIDs[0][0])

    print("Saving Segmented Image")
    fig, ax = plt.subplots(1)
    ax.imshow(clusteredImg, cmap=colorMap)
    circle = patches.Circle((x, y), 4, linewidth=1,
                            edgecolor='r', facecolor='r')
    ax.add_patch(circle)
    imgName = './outputImages/%s_ClusteredImage.jpg' % i
    plt.savefig(imgName)
