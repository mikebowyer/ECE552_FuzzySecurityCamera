
# External Library Imports
from picamera import PiCamera
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# Internal Library Imports
from lib import fuzzy_clustering as fcm
from lib import centroid_calculator as cc


# Camera Parametesr and Initialization
print("Intialization Camera")
camera = PiCamera()
camera.rotation = 0
img_width = 320
img_height = 240
camera.resolution = (img_width, img_height)

for i in range(5):
    print("Taking Image Number: %s" % i)
    # camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    im = Image.fromarray(output)
    print("Saving Original Image")
    im.save('./outputImages/%s_OriginalImage.jpg' % i)

    clusteredImg = fcm.fuzzyClusteringOnImage(output, camera.resolution)

    clusteredImgWCentroid, x, y = cc.findBrightClusterCenter(clusteredImg)

    print("Saving Segmented Image")
    fig, ax = plt.subplots(1)
    ax.imshow(clusteredImg)
    circle = patches.Circle((x, y), 4, linewidth=1,
                            edgecolor='r', facecolor='none')
    ax.add_patch(circle)
    imgName = './outputImages/%s_ClusteredImage.jpg' % i
    plt.savefig(imgName)

    # plt.imshow(clusteredImg)
    # plt.scatter(x, y, s=500, c='red', marker='o')
    # plt.show()
    # plt.imsave(imgName)
