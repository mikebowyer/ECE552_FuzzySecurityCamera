from picamera import PiCamera
from time import sleep
import numpy as np
from PIL import Image

# Camera Parametesr and Initialization
camera = PiCamera()
camera.rotation = 0
img_width = 320
img_height = 240
camera.resolution = (img_width, img_height)

for i in range(2):
    sleep(5)
    # camera.capture('/home/pi/Desktop/image%s.jpg' % i)
    output = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(output, 'rgb')
    im = Image.fromarray(output)
    im.save('/home/pi/Desktop/image%s.jpg' % i)
