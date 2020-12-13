import cv2
from time import sleep

# initialize the camera
cam = cv2.VideoCapture(1)
sleep(2)
for i in range(0, 10):
    ret, image = cam.read()


if ret:
    print("Made it")
    cv2.waitKey(0)
    cv2.imwrite('/home/pi/SnapshotTest.jpg', image)
cam.release()
