
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.patches as mpatches
from lib import fuzzy_clustering as fcm


def saveClusteredImg(img, brightestClustIDs, fileName, imgCenter, brightClustCenter, saveImg, showImg):
    # Establish color map
    colorMap = fcm.createColorMap(brightestClustIDs)

    plt.figure("2) Clustered Image")
    # Create image to save
    ax = plt.gca()
    plt.cla()
    ax.imshow(img, cmap=colorMap)
    clusterCenterCircle = patches.Circle((brightClustCenter[0], brightClustCenter[1]), 4, linewidth=1,
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
    if(saveImg):
        plt.savefig(fileName, bbox_inches='tight')
    if(showImg):
        # plt.figure("2) Clustered Image")
        plt.tight_layout()
        plt.draw()
        plt.pause(0.001)


def capturePic(cam):
    ret = 0
    image = 0
    latestImg = 0
    for i in range(0, 4):
        cam.grab()
    ret, image = cam.read()
    return ret, image


def warmUpCamera(cam):
    ret = 0
    image = 0
    for i in range(0, 10):
        ret, image = cam.read()
    return ret, image
