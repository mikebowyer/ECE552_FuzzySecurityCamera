
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
cam = cv2.VideoCapture(1)
img_width = 320
img_height = 240
cam.set(3, img_width)
cam.set(4, img_height)

# print("Intialization Camera")
# camera = PiCamera()
# camera.rotation = 0
# camera.resolution = (img_width, img_height)

for i in range(5):
    print("Taking Image Number: %s" % i)
    ret, img = capturePic(cam)
    imgToSave = Image.fromarray(img)
    print("Saving Original Image")
    imgToSave.save('./outputImages/%s_OriginalImage.jpg' % i)

    # output = np.empty((240, 320, 3), dtype=np.uint8)
    # camera.capture(output, 'rgb')

    # clusteredImg, brightestClustIDs = fcm.fuzzyClusteringOnImage(
    #     output, camera.resolution)

    # x, y = cc.findBrightClusterCenter(
    #     clusteredImg, brightestClustIDs[0][0])

    # print("Saving Segmented Image")
    # fig, ax = plt.subplots(1)
    # ax.imshow(clusteredImg)
    # circle = patches.Circle((x, y), 4, linewidth=1,
    #                         edgecolor='r', facecolor='none')
    # ax.add_patch(circle)
    # imgName = './outputImages/%s_ClusteredImage.jpg' % i
    # plt.savefig(imgName)

    # plt.imshow(clusteredImg)
    # plt.scatter(x, y, s=500, c='red', marker='o')
    # plt.show()
    # plt.imsave(imgName)
