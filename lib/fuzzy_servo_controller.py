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
        # Generate universe variables
        #   * Quality and service on subjective ranges [0, 10]
        #   * Tip has a range of [0, 25] in units of percentage points
        range_pixFromCenterErr = np.arange(-160, 160, 1)
        range_servoAngleChange = np.arange(-10, 10, 1)

        # Generate fuzzy membership functions for Inputs
        pixFromCenterErr_VeryLeft = fuzz.trimf(
            range_pixFromCenterErr, [-240, -160, -96.1])
        pixFromCenterErr_Left = fuzz.trimf(
            range_pixFromCenterErr, [-160, -80, 0])
        pixFromCenterErr_Center = fuzz.trimf(
            range_pixFromCenterErr, [-80, 0, 80])
        pixFromCenterErr_Right = fuzz.trimf(
            range_pixFromCenterErr, [0, 80, 160])
        pixFromCenterErr_VeryRight = fuzz.trimf(
            range_pixFromCenterErr, [80, 160, 240])

        # Generate fuzzy membership functions for Output
        servoAngleChange_VeryLeft = fuzz.trimf(
            range_servoAngleChange, [-15, -10, -5])
        servoAngleChange_Left = fuzz.trimf(
            range_servoAngleChange, [-10, -5, 0])
        servoAngleChange_DontMove = fuzz.trimf(
            range_servoAngleChange, [-5, 0, 5])
        servoAngleChange_Right = fuzz.trimf(range_servoAngleChange, [0, 5, 10])
        servoAngleChange_VeryRight = fuzz.trimf(
            range_servoAngleChange, [5, 10, 15])

        if(plotOrNot):
            # Visualize these universes and membership functions
            fig, (ax0, ax1) = plt.subplots(nrows=2)  # , figsize=(8, 9))

            ax0.plot(range_pixFromCenterErr, pixFromCenterErr_VeryLeft,
                     color='b', linewidth=1.5, label='Very Left')
            ax0.plot(range_pixFromCenterErr, pixFromCenterErr_Left,
                     'c', linewidth=1.5, label='Left')
            ax0.plot(range_pixFromCenterErr, pixFromCenterErr_Center,
                     'g', linewidth=1.5, label='Center')
            ax0.plot(range_pixFromCenterErr, pixFromCenterErr_Right,
                     'y', linewidth=1.5, label='Right')
            ax0.plot(range_pixFromCenterErr, pixFromCenterErr_VeryRight,
                     'r', linewidth=1.5, label='Very Right')
            ax0.set_title(
                'Input - Pixels From Center Error Horizontal Membership Functions')
            ax0.legend()

            ax1.plot(range_servoAngleChange, servoAngleChange_VeryLeft,
                     'b', linewidth=1.5, label='Very Left')
            ax1.plot(range_servoAngleChange, servoAngleChange_Left,
                     'c', linewidth=1.5, label='Left')
            ax1.plot(range_servoAngleChange, servoAngleChange_DontMove,
                     'g', linewidth=1.5, label='Do not move')
            ax1.plot(range_servoAngleChange, servoAngleChange_Right,
                     'y', linewidth=1.5, label='Right')
            ax1.plot(range_servoAngleChange, servoAngleChange_VeryRight,
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
