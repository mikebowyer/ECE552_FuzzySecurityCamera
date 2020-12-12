# External Library Imports
import cv2
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as mpatches
import logging
# Internal Library Imports
from lib import fuzzy_clustering as fcm
from lib import centroid_calculator as cc

logging.basicConfig(
    format='[%(levelname)s\t%(asctime)s] %(message)s', datefmt='%I:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('matplotlib.font_manager').disabled = True


def capturePic(cam):
    ret = 0
    image = 0
    for i in range(0, 5):
        ret, image = cam.read()
    return ret, image


def saveClusteredImg(img, clusterIds, fileName, imgCenter, brightClustCenter):
    # Establish color map
    colorMap = fcm.createColorMap(brightestClustIDs)

    # Create image to save
    fig, ax = plt.subplots(1)
    ax.imshow(clusteredImg, cmap=colorMap)
    clusterCenterCircle = patches.Circle((x, y), 4, linewidth=1,
                                         edgecolor='r', facecolor='r', label="Bright cluster center")
    ax.add_patch(clusterCenterCircle)
    imgCenterCircle = patches.Circle((imgCenter[0], imgCenter[1]), 4, linewidth=1,
                                     edgecolor='g', facecolor='g', label="Image center")
    ax.add_patch(imgCenterCircle)

    # Create Title
    brightStr = "Image center coordinates: ({}, {})".format(
        imgCenter[0], imgCenter[1])
    centerStr = "Bright cluster center coordinates: ({}, {})".format(
        brightClustCenter[0], brightClustCenter[1])
    correctionStc = "Difference between centers: ({}, {})".format(
        brightClustCenter[0] - imgCenter[0], brightClustCenter[1] - imgCenter[1])
    textstr = '\n'.join((brightStr, centerStr, correctionStc))
    plt.title(textstr)

    # Create Legend
    whitePatch = mpatches.Patch(color='white', label='Brightest cluster')
    greyPatch = mpatches.Patch(color='grey', label='Semi-bright cluster')
    blackPatch = mpatches.Patch(color='black', label='Dark cluster')
    legend1 = ax.legend(handles=[whitePatch, greyPatch, blackPatch],
                        bbox_to_anchor=(1.35, 1), facecolor='moccasin')
    legend2 = ax.legend(handles=[clusterCenterCircle, imgCenterCircle],
                        bbox_to_anchor=(1.35, .8), facecolor='moccasin')
    # Manually add the first legend back
    ax.add_artist(legend1)
    # save image
    plt.savefig(imgName, bbox_inches='tight')


# Camera Parametesr and Initialization
logging.info("Initializing Camera")
cam = cv2.VideoCapture(1)
img_width = 320
img_height = 240
img_center = [math.floor(img_width/2), math.floor(img_height/2)]
cam.set(3, img_width)
cam.set(4, img_height)

for i in range(5):
    logging.info("Capturing Image Number - %s" % i)
    ret, imgArray = capturePic(cam)

    logging.debug("Saving Original Image")
    decodedImg = Image.fromarray(imgArray)
    decodedImg.save('./outputImages/%s_OriginalImage.jpg' % i)

    logging.debug("Starting fuzzy c means clustering")
    clusteredImg, brightestClustIDs = fcm.fuzzyClusteringOnImage(
        imgArray, [img_width, img_height])

    logging.debug("Calculating center of brightest cluster")
    x, y = cc.findBrightClusterCenter(
        clusteredImg, brightestClustIDs[0][0])
    logging.info(
        "The brightest cluster center is at coordinates: ({},{})".format(x, y))

    logging.info("Saving Segmented Image")
    imgName = './outputImages/%s_ClusteredImage.jpg' % i
    saveClusteredImg(clusteredImg, brightestClustIDs,
                     imgName, img_center, [x, y])
