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
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show


class fuzzyServoSetPointChangeCalc:
    def __init__(self):

        plotOrNot = True
        self.createhorizontalMembershipFunctions(plotOrNot)

        self.calcInputMemFuncActivations(-160)

    def createhorizontalMembershipFunctions(self, plotOrNot):
        # Generate input and output analog variable ranges
        self.range_pixFromCenterErrHorz = np.arange(-160, 160, 1)
        self.range_servoAngleChangeHorz = np.arange(-10, 10, 1)

        # Generate fuzzy membership functions for Inputs
        self.mf_pixFromCenterErrHorz_VeryLeft = fuzz.trimf(
            self.range_pixFromCenterErrHorz, [-240, -160, -96.1])
        self.mf_pixFromCenterErrHorz_Left = fuzz.trimf(
            self.range_pixFromCenterErrHorz, [-160, -80, 0])
        self.mf_pixFromCenterErrHorz_Center = fuzz.trimf(
            self.range_pixFromCenterErrHorz, [-80, 0, 80])
        self.mf_pixFromCenterErrHorz_Right = fuzz.trimf(
            self.range_pixFromCenterErrHorz, [0, 80, 160])
        self.mf_pixFromCenterErrHorz_VeryRight = fuzz.trimf(
            self.range_pixFromCenterErrHorz, [80, 160, 240])

        # Generate fuzzy membership functions for Output
        self.mf_servoAngleChangeHorz_VeryLeft = fuzz.trimf(
            self.range_servoAngleChangeHorz, [-15, -10, -5])
        self.mf_servoAngleChangeHorz_Left = fuzz.trimf(
            self.range_servoAngleChangeHorz, [-10, -5, 0])
        self.mf_servoAngleChangeHorz_DontMove = fuzz.trimf(
            self.range_servoAngleChangeHorz, [-5, 0, 5])
        self.mf_servoAngleChangeHorz_Right = fuzz.trimf(
            self.range_servoAngleChangeHorz, [0, 5, 10])
        self.mf_servoAngleChangeHorz_VeryRight = fuzz.trimf(
            self.range_servoAngleChangeHorz, [5, 10, 15])

        if(plotOrNot):
            # Visualize these universes and membership functions
            fig, (ax0, ax1) = plt.subplots(nrows=2)  # , figsize=(8, 9))

            ax0.plot(self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_VeryLeft,
                     color='b', linewidth=1.5, label='Very Left')
            ax0.plot(self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Left,
                     'c', linewidth=1.5, label='Left')
            ax0.plot(self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Center,
                     'g', linewidth=1.5, label='Center')
            ax0.plot(self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Right,
                     'y', linewidth=1.5, label='Right')
            ax0.plot(self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_VeryRight,
                     'r', linewidth=1.5, label='Very Right')
            ax0.set_title(
                'Input - Pixels From Center Error Horizontal Membership Functions')
            ax0.legend()

            ax1.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryLeft,
                     'b', linewidth=1.5, label='Very Left')
            ax1.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Left,
                     'c', linewidth=1.5, label='Left')
            ax1.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_DontMove,
                     'g', linewidth=1.5, label='Do not move')
            ax1.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Right,
                     'y', linewidth=1.5, label='Right')
            ax1.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryRight,
                     'r', linewidth=1.5, label='Very Right')
            ax1.set_title(
                'Output - Degrees to Move Horizontal Membership Functions')
            ax1.legend()

            # Turn off top/right axes
            for ax in (ax0, ax1):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            plt.tight_layout()
            plt.draw()
            plt.show()

    def calcInputMemFuncActivations(self, pixFromCenterErrHorz):
        self.act_pixFromCenterErrHorz_VeryLeft = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_VeryLeft, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Left = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Left, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Center = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Center, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Right = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Right, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_VeryRight = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Left, pixFromCenterErrHorz)
