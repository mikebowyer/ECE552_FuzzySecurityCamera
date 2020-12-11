##################################################
# ECE 552 - Security Camera Start Script
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


def fuzzyClusteringOnImage(inputImage, camRes):
    colors = ['black', 'orange', 'grey']

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
        mydata, c=numClusters, m=2, error=0.005, maxiter=1000)

    numPixels = len(u[0, :])
    pixelClassification = np.empty(numPixels)
    for j in range(0, numPixels):
        pixelClassification[j] = u[:, j].argmax()

    pixelClassifiedImage = pixelClassification.reshape(
        camRes.height, camRes.width)

    return pixelClassifiedImage
