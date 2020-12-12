import RPi.GPIO as GPIO
from time import sleep


def getDutyFromAngle(angle):
    duty = (angle/18) + 7
    return duty


def controlServo(servo, gpiopin, duty):
    # print(duty)
    GPIO.output(11, True)
    GPIO.output(13, True)
    servo.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    GPIO.output(13, False)
    # servo.ChangeDutyCycle(duty)


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

leftServo = GPIO.PWM(11, 50)
rightServo = GPIO.PWM(13, 50)
leftServo.start(0)
rightServo.start(0)

leftAngle = 0
rightAngle = 0

controlServo(leftServo, 11, getDutyFromAngle(leftAngle))
controlServo(rightServo, 13, getDutyFromAngle(rightAngle))

while(1):
    usrinput = input("Angle you want servos at (p = +5 deg, l = -5 deg): ")
    # print(f'You entered {usrinput}')
    if(usrinput == "p"):
        leftAngle += 15
        rightAngle += 15
    elif(usrinput == "l"):
        leftAngle += -15
        rightAngle += -15
    else:
        leftAngle = int(usrinput)
        rightAngle = int(usrinput)

    print("Current Servo Angle: {}".format(leftAngle))

    controlServo(leftServo, 11, getDutyFromAngle(leftAngle))
    controlServo(rightServo, 13, getDutyFromAngle(rightAngle))

leftServo.stop()
rightServo.stop()
GPIO.cleanup()
