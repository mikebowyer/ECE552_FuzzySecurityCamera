##################################################
# Servo Controller Class
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
import RPi.GPIO as GPIO
from time import sleep


class ServoControl:

    def __init__(self):
        self.verticalGPIONum = 11
        self.horizontalGPIONum = 13
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.verticalGPIONum, GPIO.OUT)
        GPIO.setup(self.horizontalGPIONum, GPIO.OUT)

        self.vertServo = GPIO.PWM(self.verticalGPIONum, 50)
        self.horizServo = GPIO.PWM(self.horizontalGPIONum, 50)
        self.horizServo.start(0)
        self.vertServo.start(0)

        self.horizontalAngle = 0
        self.verticalAngle = 0
        self.controlling = 'horizontal'

        self.controlServos(
            self.verticalAngle,
            self.horizontalAngle)

    def controlServos(self, vertAngle, horizAngle):
        verticalDuty = self.getDutyFromAngle(vertAngle)
        horizontalDuty = self.getDutyFromAngle(horizAngle)

        GPIO.output(self.verticalGPIONum, True)
        GPIO.output(self.horizontalGPIONum, True)

        self.vertServo.ChangeDutyCycle(verticalDuty)
        self.horizServo.ChangeDutyCycle(horizontalDuty)
        sleep(.5)
        self.vertServo.ChangeDutyCycle(0)
        self.horizServo.ChangeDutyCycle(0)
        GPIO.output(self.verticalGPIONum, False)
        GPIO.output(self.horizontalGPIONum, False)

    def getDutyFromAngle(self, angle):
        duty = (-angle/18) + 7
        return duty

    def changeServoPosition(self, vert_servoAngleChange, horiz_seroAngleChange):
        newVertAngle = self.limitServoPosition(
            self.verticalAngle + vert_servoAngleChange)
        self.verticalAngle = newVertAngle

        newHorizAngle = self.limitServoPosition(
            self.horizontalAngle + horiz_seroAngleChange)
        self.horizontalAngle = newHorizAngle

        self.controlServos(newVertAngle, newHorizAngle)

        return self.verticalAngle, self.horizontalAngle

    def limitServoPosition(self, inputAngle):
        returnVal = 0
        if(inputAngle > 45):
            returnVal = 45
        elif(inputAngle < -45):
            returnVal = -45
        else:
            returnVal = inputAngle

        return returnVal
