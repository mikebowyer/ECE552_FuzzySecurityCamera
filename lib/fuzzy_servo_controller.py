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
        self.plotOrNot = False
        # self.plotOrNot = True
        self.createhorizontalMembershipFunctions()

    def calcChangeInServoAngles(self, vert_pixErrFromCenter, horiz_pixErrFromCenter):
        # Vertical
        # self.calcvertInputMemFuncActivations(vert_pixErrFromCenter)
        # vert_servoAngleChange = self.applyvertRulesAndDefuzzify()
        vert_servoAngleChange = 0
        # Horizontal
        self.calcHorizInputMemFuncActivations(horiz_pixErrFromCenter)
        horiz_servoAngleChange = self.applyHorizRulesAndDefuzzify()
        return vert_servoAngleChange, horiz_servoAngleChange

    def createhorizontalMembershipFunctions(self):
        # Generate input and output analog variable ranges
        self.range_pixFromCenterErrHorz = np.arange(-160, 160, 1)
        self.range_servoAngleChangeHorz = np.arange(-25, 25, .1)

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
            self.range_servoAngleChangeHorz, [-35, -25, -12.5])
        self.mf_servoAngleChangeHorz_Left = fuzz.trimf(
            self.range_servoAngleChangeHorz, [-25, -12.5, 0])
        self.mf_servoAngleChangeHorz_DontMove = fuzz.trimf(
            self.range_servoAngleChangeHorz, [-12.5, 0, 12.5])
        self.mf_servoAngleChangeHorz_Right = fuzz.trimf(
            self.range_servoAngleChangeHorz, [0, 12.5, 25])
        self.mf_servoAngleChangeHorz_VeryRight = fuzz.trimf(
            self.range_servoAngleChangeHorz, [12.5, 25, 35])

        # if(self.plotOrNot):
        if(False):
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

    def calcHorizInputMemFuncActivations(self, pixFromCenterErrHorz):
        self.act_pixFromCenterErrHorz_VeryLeft = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_VeryLeft, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Left = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Left, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Center = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Center, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_Right = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_Right, pixFromCenterErrHorz)
        self.act_pixFromCenterErrHorz_VeryRight = fuzz.interp_membership(
            self.range_pixFromCenterErrHorz, self.mf_pixFromCenterErrHorz_VeryRight, pixFromCenterErrHorz)

    def applyHorizRulesAndDefuzzify(self):
        # Rule 1 - If Very Left input, very left output
        act_rule1 = self.act_pixFromCenterErrHorz_VeryLeft
        act_servoAngleChangeHorz_VeryLeft = np.fmin(
            act_rule1, self.mf_servoAngleChangeHorz_VeryLeft)
        # Rule 2 - If Left input, left output
        act_rule2 = self.act_pixFromCenterErrHorz_Left
        act_servoAngleChangeHorz_Left = np.fmin(
            act_rule2, self.mf_servoAngleChangeHorz_Left)
        # Rule 3 - If Center input, DontMove output
        act_rule3 = self.act_pixFromCenterErrHorz_Center
        act_servoAngleChangeHorz_DontMove = np.fmin(
            act_rule3, self.mf_servoAngleChangeHorz_DontMove)
        # Rule 4 - If right input, right output
        act_rule4 = self.act_pixFromCenterErrHorz_Right
        act_servoAngleChangeHorz_Right = np.fmin(
            act_rule4, self.mf_servoAngleChangeHorz_Right)
        # Rule 5 - If Very right input, very right output
        act_rule5 = self.act_pixFromCenterErrHorz_VeryRight
        act_servoAngleChangeHorz_VeryRight = np.fmin(
            act_rule5, self.mf_servoAngleChangeHorz_VeryRight)

        act_zeros = np.zeros_like(self.range_servoAngleChangeHorz)

        if(self.plotOrNot):
            # Visualize this
            fig, ax0 = plt.subplots()

            # Plot Very Left Output Membership Values
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, act_servoAngleChangeHorz_VeryLeft,
                             facecolor='b', alpha=0.7)
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryLeft,
                     'b', linewidth=0.5, linestyle='--', )

            # Plot Left Output Membership Values
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, act_servoAngleChangeHorz_Left,
                             facecolor='c', alpha=0.7)
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Left,
                     'c', linewidth=0.5, linestyle='--', )

            # Plot Dont Move Output Membership Values
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, act_servoAngleChangeHorz_DontMove,
                             facecolor='g', alpha=0.7)
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_DontMove,
                     'g', linewidth=0.5, linestyle='--', )

            # Plot Right Output Membership Values
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, act_servoAngleChangeHorz_Right,
                             facecolor='y', alpha=0.7)
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Right,
                     'y', linewidth=0.5, linestyle='--', )

            # Plot Very Right Output Membership Values
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, act_servoAngleChangeHorz_VeryRight,
                             facecolor='r', alpha=0.7)
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryRight,
                     'r', linewidth=0.5, linestyle='--', )
            ax0.set_title(
                'Membership values of output membership functions after rule application')
            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            plt.tight_layout()
            plt.draw()
            plt.show()

        # Defuzzify
        aggregated = np.fmax(act_servoAngleChangeHorz_VeryLeft, np.fmax(act_servoAngleChangeHorz_Left, np.fmax(
            act_servoAngleChangeHorz_DontMove, np.fmax(act_servoAngleChangeHorz_Right, act_servoAngleChangeHorz_VeryRight))))

        output_servoAngleChangeHorz = fuzz.defuzz(self.range_servoAngleChangeHorz,
                                                  aggregated, 'centroid')

        if(self.plotOrNot):
            output_activation = fuzz.interp_membership(
                self.range_servoAngleChangeHorz, aggregated, output_servoAngleChangeHorz)  # for plot

            # Visualize this
            fig, ax0 = plt.subplots()

            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryLeft,
                     'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Left,
                     'c', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_DontMove,
                     'g', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_Right,
                     'y', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChangeHorz, self.mf_servoAngleChangeHorz_VeryRight,
                     'r', linewidth=0.5, linestyle='--')
            ax0.fill_between(self.range_servoAngleChangeHorz, act_zeros, aggregated,
                             facecolor='Orange', alpha=0.7)
            ax0.plot([output_servoAngleChangeHorz, output_servoAngleChangeHorz], [0, output_activation],
                     'k', linewidth=1.5, alpha=0.9)
            ax0.set_title('Aggregated membership and result (line)')

            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            plt.tight_layout()
            plt.draw()
            plt.show()

        return output_servoAngleChangeHorz
