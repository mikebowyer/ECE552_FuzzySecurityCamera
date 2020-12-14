##################################################
# Centroid Calculation of fuzzy clustered image
##################################################
# GNU GENERAL PUBLIC LICENSE
##################################################
# Author: Michael Bowyer
# Maintainer: Michael Bowyer
# Email: mbowyer@umich.edu
# License: GNU GENERAL PUBLIC LICENSE
##################################################

import numpy as np
import math


def findBrightClusterCenter(inputImg, brightestClusterID):
    # Grab all x and y coordinates of pixels which contain the #2
    brightPixelCoordinates = np.where(inputImg == brightestClusterID)
    centroid_center_vert = math.floor(brightPixelCoordinates[0].mean())
    centroid_center_horiz = math.floor(brightPixelCoordinates[1].mean())

    centroid_std_vert = math.floor(brightPixelCoordinates[0].std())
    centroid_std_horiz = math.floor(brightPixelCoordinates[1].std())

    # inputImg[centroidY][centroidX] = 4

    return centroid_center_horiz, centroid_center_vert, centroid_std_horiz, centroid_std_vert
