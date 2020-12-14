##################################################
# Calculation of servo position using fuzzy logic
##################################################
# GNU GENERAL PUBLIC LICENSE
##################################################
# Author: Michael Bowyer
# Maintainer: Michael Bowyer
# Email: mbowyer@umich.edu
# License: GNU GENERAL PUBLIC LICENSE
##################################################

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show


class fuzzyServoSetPointChangeCalc:
    def __init__(self, saveFuzzImg, showFuzzImg):
        self.plotOrNot = showFuzzImg
        self.saveOrNot = saveFuzzImg
        self.saveFilePath = "./outputImages/fuzzyOutputs/"
        # self.plotOrNot = True
        self.createMembershipFunctions()

    def calcChangeInServoAngles(self, vert_pixErrFromCenter, horiz_pixErrFromCenter, brightClust_std_horiz, brightClust_std_vert, percentPixelsInBrightestClust):
        # Vertical
        self.calcInputMemFuncActivations(
            vert_pixErrFromCenter, brightClust_std_vert, percentPixelsInBrightestClust)
        vert_servoAngleChange = self.applyRulesAndDefuzzify(
            'vertical', vert_pixErrFromCenter)
        # Horizontal
        self.calcInputMemFuncActivations(
            horiz_pixErrFromCenter, brightClust_std_horiz, percentPixelsInBrightestClust)
        horiz_servoAngleChange = self.applyRulesAndDefuzzify(
            'horizontal', horiz_pixErrFromCenter)
        return vert_servoAngleChange, horiz_servoAngleChange

    def createMembershipFunctions(self):
        # Generate input and output analog variable ranges
        self.range_pixFromCenterErr = np.arange(-160, 160, 1)
        self.range_brightClustStd = np.arange(0, 160, 1)
        self.range_brightClustPixPct = np.arange(0, 100, 1)
        self.range_servoAngleChange = np.arange(-25, 25, .1)

        # Pixel-From-Center-Error - Generate fuzzy membership functions for Variable
        self.mf_pixFromCenterErr_VeryLeft = fuzz.trimf(
            self.range_pixFromCenterErr, [-240, -160, -96.1])
        self.mf_pixFromCenterErr_Left = fuzz.trimf(
            self.range_pixFromCenterErr, [-160, -80, 0])
        self.mf_pixFromCenterErr_Center = fuzz.trimf(
            self.range_pixFromCenterErr, [-80, 0, 80])
        self.mf_pixFromCenterErr_Right = fuzz.trimf(
            self.range_pixFromCenterErr, [0, 80, 160])
        self.mf_pixFromCenterErr_VeryRight = fuzz.trimf(
            self.range_pixFromCenterErr, [80, 160, 240])

        #  Percent-Of-Pixels-In-Brightest-Cluster - Generate fuzzy membership functions for Variable
        self.mf_pctPixBright_Few = fuzz.trapmf(
            self.range_brightClustPixPct,  [-20, 0, 20, 40])
        self.mf_pctPixBright_Many = fuzz.trapmf(
            self.range_brightClustPixPct,  [20, 40, 60, 80])
        self.mf_pctPixBright_TooMany = fuzz.trapmf(
            self.range_brightClustPixPct,  [60, 80, 100, 120])

        #   Brightest-Cluster-Standard-Deviation - Generate fuzzy membership functions for Variable
        self.mf_brightClustStd_Low = fuzz.trapmf(
            self.range_brightClustStd,  [-20, 0, 32, 64])
        self.mf_brightClustStd_Med = fuzz.trapmf(
            self.range_brightClustStd,  [32, 64, 96, 128])
        self.mf_brightClustStd_High = fuzz.trapmf(
            self.range_brightClustStd,  [96, 128, 160, 220])

        # Generate fuzzy membership functions for Output
        self.mf_servoAngleChange_VeryLeft = fuzz.trimf(
            self.range_servoAngleChange, [-35, -25, -12.5])
        self.mf_servoAngleChange_Left = fuzz.trimf(
            self.range_servoAngleChange, [-25, -12.5, 0])
        self.mf_servoAngleChange_DontMove = fuzz.trimf(
            self.range_servoAngleChange, [-12.5, 0, 12.5])
        self.mf_servoAngleChange_Right = fuzz.trimf(
            self.range_servoAngleChange, [0, 12.5, 25])
        self.mf_servoAngleChange_VeryRight = fuzz.trimf(
            self.range_servoAngleChange, [12.5, 25, 35])

        # if(self.plotOrNot):
        if(self.saveOrNot):
            # Visualize these universes and membership functions
            fig, (ax0, ax1) = plt.subplots(nrows=2)  # , figsize=(8, 9))

            ax0.plot(self.range_pixFromCenterErr, self.mf_pixFromCenterErr_VeryLeft,
                     color='b', linewidth=1.5, label='Very Left')
            ax0.plot(self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Left,
                     'c', linewidth=1.5, label='Left')
            ax0.plot(self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Center,
                     'g', linewidth=1.5, label='Center')
            ax0.plot(self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Right,
                     'y', linewidth=1.5, label='Right')
            ax0.plot(self.range_pixFromCenterErr, self.mf_pixFromCenterErr_VeryRight,
                     'r', linewidth=1.5, label='Very Right')
            ax0.set_title(
                'Input - Pixels From Center Error Horizontal Membership Functions')
            ax0.legend()

            ax1.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryLeft,
                     'b', linewidth=1.5, label='Very Left')
            ax1.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Left,
                     'c', linewidth=1.5, label='Left')
            ax1.plot(self.range_servoAngleChange, self.mf_servoAngleChange_DontMove,
                     'g', linewidth=1.5, label='Do not move')
            ax1.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Right,
                     'y', linewidth=1.5, label='Right')
            ax1.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryRight,
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
                ax.set_xlabel(
                    "Output Variable - Change in camera vertical/horizontal angle (Degrees)")
                ax.set_ylabel(
                    "Membership Amount")

            plt.tight_layout()
            # plt.draw()
            # plt.show()
            if(self.saveOrNot):
                plt.savefig(self.saveFilePath +
                            "OutputMembershipFunction", bbox_inches='tight')

    def calcInputMemFuncActivations(self, pixFromCenterErr, brightClust_std, percentPixelsInBrightestClust):
        # Pixel-From-Center-Error
        self.act_pixFromCenterErr_VeryLeft = fuzz.interp_membership(
            self.range_pixFromCenterErr, self.mf_pixFromCenterErr_VeryLeft, pixFromCenterErr)
        self.act_pixFromCenterErr_Left = fuzz.interp_membership(
            self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Left, pixFromCenterErr)
        self.act_pixFromCenterErr_Center = fuzz.interp_membership(
            self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Center, pixFromCenterErr)
        self.act_pixFromCenterErr_Right = fuzz.interp_membership(
            self.range_pixFromCenterErr, self.mf_pixFromCenterErr_Right, pixFromCenterErr)
        self.act_pixFromCenterErr_VeryRight = fuzz.interp_membership(
            self.range_pixFromCenterErr, self.mf_pixFromCenterErr_VeryRight, pixFromCenterErr)

        # Percent-Of-Pixels-In-Brightest-Cluster
        self.act_pctPixBright_Few = fuzz.interp_membership(
            self.range_brightClustPixPct, self.mf_pctPixBright_Few, percentPixelsInBrightestClust)
        self.act_pctPixBright_Many = fuzz.interp_membership(
            self.range_brightClustPixPct, self.mf_pctPixBright_Many, percentPixelsInBrightestClust)
        self.act_pctPixBright_TooMany = fuzz.interp_membership(
            self.range_brightClustPixPct, self.mf_pctPixBright_TooMany, percentPixelsInBrightestClust)

        # Brightest-Cluster-Standard-Deviation
        self.act_brightClustStd_Low = fuzz.interp_membership(
            self.range_brightClustStd, self.mf_brightClustStd_Low, brightClust_std)
        self.act_brightClustStd_Med = fuzz.interp_membership(
            self.range_brightClustStd, self.mf_brightClustStd_Med, brightClust_std)
        self.act_brightClustStd_High = fuzz.interp_membership(
            self.range_brightClustStd, self.mf_brightClustStd_High, brightClust_std)

    def applyRulesAndDefuzzify(self, horizOrVert, pixFromCenter):
        # Rule 1 - If Very Left input, very left output
        act_rule1 = self.act_pixFromCenterErr_VeryLeft
        act_servoAngleChange_VeryLeft = np.fmin(
            act_rule1, self.mf_servoAngleChange_VeryLeft)
        # Rule 2 - If Left input, left output
        act_rule2 = self.act_pixFromCenterErr_Left
        act_servoAngleChange_Left = np.fmin(
            act_rule2, self.mf_servoAngleChange_Left)
        # Rule 3 - If Center input, DontMove output
        act_rule3 = self.act_pixFromCenterErr_Center
        act_servoAngleChange_DontMove = np.fmin(
            act_rule3, self.mf_servoAngleChange_DontMove)
        # Rule 4 - If right input, right output
        act_rule4 = self.act_pixFromCenterErr_Right
        act_servoAngleChange_Right = np.fmin(
            act_rule4, self.mf_servoAngleChange_Right)
        # Rule 5 - If Very right input, very right output
        act_rule5 = self.act_pixFromCenterErr_VeryRight
        act_servoAngleChange_VeryRight = np.fmin(
            act_rule5, self.mf_servoAngleChange_VeryRight)
        # Rule 6 - If Too Many Pixels OR High Pixel Standard deviation, Don't Move (Weight of 1)
        act_rule6 = np.fmax(self.act_pctPixBright_TooMany,
                            self.act_brightClustStd_High)
        act_servoAngleChange_DontMove_2 = np.fmin(
            act_rule6, self.mf_servoAngleChange_DontMove)

        # Rule 7 - If Many Pixels OR Medium Pixel Standard deviation, Don't Move (Weight of .5)
        act_rule7 = np.fmax(self.act_pctPixBright_Many,
                            self.act_brightClustStd_Med)*.5
        act_servoAngleChange_DontMove_3 = np.fmin(
            act_rule7, self.mf_servoAngleChange_DontMove)

        act_zeros = np.zeros_like(self.range_servoAngleChange)

        if(self.plotOrNot or self.saveOrNot):
            # Visualize this
            fileName = " "
            if(horizOrVert == 'vertical'):
                plt.figure("3a) Vertical Axis Rule Application Result")
                fileName = "3a) Vertical Axis Rule Application Result"
            else:
                plt.figure("3b) Horizontal Axis Rule Application Result")
                fileName = "3b) Horizontal Axis Rule Application Result"
            ax0 = plt.gca()
            plt.cla()

            # Plot Very Left Output Membership Values
            ax0.fill_between(self.range_servoAngleChange, act_zeros, act_servoAngleChange_VeryLeft,
                             facecolor='b', alpha=0.7)
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryLeft,
                     'b', linewidth=0.5, linestyle='--', )

            # Plot Left Output Membership Values
            ax0.fill_between(self.range_servoAngleChange, act_zeros, act_servoAngleChange_Left,
                             facecolor='c', alpha=0.7)
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Left,
                     'c', linewidth=0.5, linestyle='--', )

            # Plot Dont Move Output Membership Values
            act_servoAngleChange_max = np.fmax(act_servoAngleChange_DontMove, np.fmax(
                act_servoAngleChange_DontMove_2, act_servoAngleChange_DontMove_3))
            ax0.fill_between(self.range_servoAngleChange, act_zeros, act_servoAngleChange_max,
                             facecolor='g', alpha=0.7)
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_DontMove,
                     'g', linewidth=0.5, linestyle='--', )

            # Plot Right Output Membership Values
            ax0.fill_between(self.range_servoAngleChange, act_zeros, act_servoAngleChange_Right,
                             facecolor='y', alpha=0.7)
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Right,
                     'y', linewidth=0.5, linestyle='--', )

            # Plot Very Right Output Membership Values
            ax0.fill_between(self.range_servoAngleChange, act_zeros, act_servoAngleChange_VeryRight,
                             facecolor='r', alpha=0.7)
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryRight,
                     'r', linewidth=0.5, linestyle='--', )

            titleStr = " "
            if(horizOrVert == 'vertical'):
                titleStr = 'Rule application result - \nBright cluster center {} pixels from the center vertically'.format(
                    pixFromCenter)
                ax0.set_xlabel(
                    "Output Variable - Change in camera vertical angle (Degrees)")
            else:
                titleStr = 'Rule application result - \nBright cluster center {} pixels from the center horizontally'.format(
                    pixFromCenter)
                ax0.set_xlabel(
                    "Output Variable - Change in camera horizontal angle (Degrees)")

            ax0.set_title(titleStr)
            ax0.legend()
            ax0.set_ylabel("Membership Amount")
            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            if(self.saveOrNot):
                plt.savefig(self.saveFilePath + fileName,
                            bbox_inches='tight')
            if(self.plotOrNot):
                plt.tight_layout()
                plt.draw()
                plt.pause(0.001)

        # Defuzzify
        aggregated = np.fmax(act_servoAngleChange_VeryLeft, np.fmax(act_servoAngleChange_Left, np.fmax(
            act_servoAngleChange_DontMove, np.fmax(act_servoAngleChange_Right, np.fmax(act_servoAngleChange_VeryRight, np.fmax(act_servoAngleChange_DontMove_2, act_servoAngleChange_DontMove_3))))))

        output_servoAngleChange = fuzz.defuzz(self.range_servoAngleChange,
                                              aggregated, 'centroid')

        if(self.plotOrNot):
            output_activation = fuzz.interp_membership(
                self.range_servoAngleChange, aggregated, output_servoAngleChange)  # for plot
            fileName = " "
            if(horizOrVert == 'vertical'):
                plt.figure("4a) Vertical Axis Defuzzification Result")
                fileName = "4a) Vertical Axis Defuzzification Result"
            else:
                plt.figure("4b) Horizontal Axis Defuzzification Result")
                fileName = "4b) Horizontal Axis Defuzzification Result"
            ax0 = plt.gca()
            plt.cla()

            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryLeft,
                     'b', linewidth=0.5, linestyle='--', )
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Left,
                     'c', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_DontMove,
                     'g', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_Right,
                     'y', linewidth=0.5, linestyle='--')
            ax0.plot(self.range_servoAngleChange, self.mf_servoAngleChange_VeryRight,
                     'r', linewidth=0.5, linestyle='--')
            ax0.fill_between(self.range_servoAngleChange, act_zeros, aggregated,
                             facecolor='Orange', alpha=0.7)
            ax0.plot([output_servoAngleChange, output_servoAngleChange], [0, output_activation],
                     'k', linewidth=1.5, alpha=0.9)

            if(horizOrVert == 'vertical'):
                ax0.set_title(
                    'Defuzzification result - \nBright cluster center {} pixels from the center vertically'.format(pixFromCenter))
                ax0.set_xlabel(
                    "Output Variable - Change in camera vertical angle (Degrees)")
            else:
                ax0.set_title(
                    'Defuzzification result - \nBright cluster center {} pixels from the center horizontally'.format(pixFromCenter))
                ax0.set_xlabel(
                    "Output Variable - Change in camera horizontal angle (Degrees)")
            ax0.legend()
            ax0.set_ylabel("Membership Amount")

            # Turn off top/right axes
            for ax in (ax0,):
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.get_xaxis().tick_bottom()
                ax.get_yaxis().tick_left()

            if(self.saveOrNot):
                plt.savefig(self.saveFilePath + fileName,
                            bbox_inches='tight')
            if(self.plotOrNot):
                plt.tight_layout()
                plt.draw()
                plt.pause(0.001)

        return output_servoAngleChange
