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
from lib import img_tools as imgtls
from lib import servo_control as servoControl
from lib import fuzzy_servo_controller as fsc

############################
### Setup logging config ###
############################
logging.basicConfig(
    format='[%(levelname)s\t%(asctime)s] %(message)s', datefmt='%I:%M:%S')
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger('matplotlib.font_manager').disabled = True

############################
# Setup Servo Controller and set point calculator
############################
servoController = servoControl.ServoControl()
fuzzyServoSetPointCalc = fsc.fuzzyServoSetPointChangeCalc()


############################
# Camera Parametesr and Initialization
############################
logging.info("Initializing Camera")
cam = cv2.VideoCapture(0)
img_width = 320
img_height = 240
img_center = [math.floor(img_width/2), math.floor(img_height/2)]
cam.set(3, img_width)
cam.set(4, img_height)
imgtls.warmUpCamera(cam)


############################
# Start Control Loop
############################
for i in range(5):
    logging.info("Capturing Image Number - %s" % i)
    ret, imgArray = imgtls.capturePic(cam)

    logging.debug("Saving Original Image")
    decodedImg = Image.fromarray(imgArray)
    decodedImg.save('./outputImages/%s_OriginalImage.jpg' % i)

    logging.debug("Starting fuzzy c means clustering")
    clusteredImg, brightestClustIDs = fcm.fuzzyClusteringOnImage(
        imgArray, [img_width, img_height])

    logging.debug("Calculating center of brightest cluster")
    brightClust_x, brightClust_y = cc.findBrightClusterCenter(
        clusteredImg, brightestClustIDs[0][0])
    logging.info(
        "The brightest cluster center is at coordinates: ({},{})".format(brightClust_x, brightClust_y))

    logging.debug("Calculating set point for Servos")
    vert_pixErrFromCenter = brightClust_y - img_center[1]
    horiz_pixErrFromCenter = brightClust_x - img_center[0]

    vert_servoAngleChange, horiz_seroAngleChange = fuzzyServoSetPointCalc.calcChangeInServoAngles(
        vert_pixErrFromCenter, horiz_pixErrFromCenter)

    logging.info("Controlling servos to new setpoint")
    currentVerticalAngle, currentHorizontalAngle = servoController.changeServoPosition(
        vert_servoAngleChange, horiz_seroAngleChange)
    logging.info("New servo motor positions are \tVertical: {}\tHorizontal:{}".format(
        currentVerticalAngle, currentHorizontalAngle))

    logging.debug("Saving Segmented Image")
    imgName = './outputImages/%s_ClusteredImage.jpg' % i
    imgtls.saveClusteredImg(clusteredImg, brightestClustIDs,
                            imgName, img_center, [brightClust_x, brightClust_y])
