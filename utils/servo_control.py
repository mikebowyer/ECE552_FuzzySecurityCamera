import RPi.GPIO as GPIO
from time import sleep


def getDutyFromAngle(angle):
    duty = (-angle/18) + 7
    return duty


def controlServo(servo, gpiopin, duty):
    GPIO.output(11, True)
    GPIO.output(13, True)
    servo.ChangeDutyCycle(duty)
    sleep(.5)
    GPIO.output(11, False)
    GPIO.output(13, False)
    servo.ChangeDutyCycle(0)


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

vertServo = GPIO.PWM(11, 50)
horizServo = GPIO.PWM(13, 50)
horizServo.start(0)
vertServo.start(0)

horizontalAngle = 0
verticalAngle = 0
controlling = 'horizontal'

controlServo(horizServo, 11, getDutyFromAngle(horizontalAngle))
controlServo(vertServo, 13, getDutyFromAngle(verticalAngle))

while(1):
    usrinput = input("Angle you want servos at (p = +5 deg, l = -5 deg): ")
    # print(f'You entered {usrinput}')
    if(usrinput == "v"):
        controlling = "vertical"
    elif(usrinput == "h"):
        controlling = "horizontal"
    else:
        if(usrinput == "p"):
            if(controlling == "horizontal"):
                horizontalAngle += 15
            else:
                verticalAngle += 15
        elif(usrinput == "l"):
            if(controlling == "horizontal"):
                horizontalAngle += -15
            else:
                verticalAngle += -15
        else:
            if(controlling == "horizontal"):
                horizontalAngle = int(usrinput)
            else:
                verticalAngle = int(usrinput)

    print("Vertical Servo Angle: {}".format(verticalAngle))
    print("Horizontal Servo Angle: {}".format(horizontalAngle))

    controlServo(horizServo, 11, getDutyFromAngle(horizontalAngle))
    controlServo(vertServo, 13, getDutyFromAngle(verticalAngle))

horizServo.stop()
vertServo.stop()
GPIO.cleanup()
