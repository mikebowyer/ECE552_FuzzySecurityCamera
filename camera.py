from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 0

for i in range(5):
    sleep(5)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()