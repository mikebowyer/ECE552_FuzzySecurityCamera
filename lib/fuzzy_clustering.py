##################################################
# Fuzzy C means clustering implementation
##################################################
# {License_info}
##################################################
# Author: Michael Bowyer
# Maintainer: Michael Bowyer
# Email: mbowyer@umich.edu
# Copyright: Copyright {year}, {project_name}
# Credits:
# Version: {mayor}.{minor}.{rel}
## License: {license}
## Status: {dev_status}
##################################################
import numpy as np
import skfuzzy as fuzz
from matplotlib import colors


def findBrightestCluster(clusterRGBCenters):
    rgbMeans = [[0, clusterRGBCenters[0].mean()],
                [1, clusterRGBCenters[1].mean()],
                [2, clusterRGBCenters[2].mean()]]
    rgbMeans.sort(key=lambda x: x[1])  # in places
    rgbMeans.reverse()
    return rgbMeans


def fuzzyClusteringOnImage(inputImage, imgRes):
    # colors = ['black', 'orange', 'grey']

    # Define three cluster centers and parameters
    centers = [[0, 0, 0],
               [122, 122, 122],
               [255, 255, 255]]
    numClusters = 3
    maxIter = 100

    redPixelValues = inputImage[:, :, 0].flatten()
    greenPixelValues = inputImage[:, :, 1].flatten()
    bluePixelValues = inputImage[:, :, 2].flatten()
    mydata = np.vstack((redPixelValues, greenPixelValues, bluePixelValues))
    cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
        mydata, c=numClusters, m=2, error=0.5, maxiter=1000)

    # Determine which cluster
    brightestClusterIDs = findBrightestCluster(cntr)
    numPixels = len(u[0, :])
    pixelClassification = np.empty(numPixels)
    for j in range(0, numPixels):
        pixelClassification[j] = u[:, j].argmax()

    pixelClassifiedImage = pixelClassification.reshape(
        imgRes[1], imgRes[0])

    return pixelClassifiedImage, brightestClusterIDs


def createColorMap(brightestClustIDs):
    colorOrder = [-1, -1, 1]

    for i in range(0, 3):
        colorId = brightestClustIDs[i][0]
        if(i == 0):
            colorOrder[colorId] = 'white'
        elif(i == 1):
            colorOrder[colorId] = 'grey'
        else:
            colorOrder[colorId] = 'black'

    cmap = colors.ListedColormap(colorOrder)
    return cmap
