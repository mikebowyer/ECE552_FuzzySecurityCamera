# ECE552_FuzzySecurityCamera
This repository contains all of the code created within scope of a graduate degree course at the University of Michigan Dearborn. 
The course is known as ECE552 "Fuzzy Systems", and was taken by Michael Bowyer (mbowyer@umich.edu) in the Fall 2020 semester. 

## Hardware Requirements
This project was desgined and ran on a Raspberry Piv4 hardware with an external USB web cam attached. There are also two Mg995 Servos  attached to the raspberry pi on GPIO pins 11 and 13. One servo controls the horizontal angle the webcam is facing, and the other controls the vertical angle. Both  servos are controlled via PWM.
## Installation
All work was done using a python 3 virtual environment on the raspberry pi. 
```bash
pip install -r environment/requirements.txt
```

## Usage

```bash
python security_cam_start.py --saveImages --showImages --saveFuzzyImages --showFuzzyImages --stopEachImg 
```

usage: security_cam_start.py [-h] [--saveImages] [--showImages]
                             [--saveFuzzyImages] [--showFuzzyImages]
                             [--stopEachImg]

Run the fuzzy security system designed for ECE 552

optional arguments:
  -h, --help         show this help message and exit
  --saveImages       Save images captured and their clustered results
  --showImages       Show images captured and their clustered results on the
                     screen
  --saveFuzzyImages  Save all fuzzy related plots
  --showFuzzyImages  Show all fuzzy related plots on the screen
  --stopEachImg      Interupt. If true, then the program will be interupted
                     and wait for user input after each image is taken.

## Contributing
Michael Bowyer (mbowyer@umich.edu)

## License
[GNU GENERAL PUBLIC LICENSE](https://choosealicense.com/licenses/gpl-3.0/)