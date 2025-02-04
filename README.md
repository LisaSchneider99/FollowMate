# FollowMate
Software for a robot that can follow people using foot bracelet

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Members](#members)
4. [Installation & Manual](#installation--manual)
5. [Structure of the code](#Structure-of-the-code)
6. [FAQ](#faq)

## General Info


This project focuses on developing an autonomous robot capable of following a person, distinguishing between multiple individuals, and stopping when the tracked person is very close.

Such a robot can assist elderly people in navigating their homes, supermarkets, or medical facilities. It can be used to carry heavy items such as groceries or bags, making daily life easier.

The goal of this project is to create a reliable and intelligent solution for person detection and tracking, providing practical assistance in everyday situations.

## Members

| Name     | E-Mail |
| :---:        |    :----:   |
| Lisa Schneider      | lisa.schneider@smail.th-koeln.de       |
| Manuel Wette   | manuel.wette@smail.th-koeln.de        |

## Technologies

A list of technologies used within the project:

### Languages:

* Python 3.11.2 or higher <https://www.python.org/>

### Libraries:

**General:**
* numpy 1.24.2 <https://pypi.org/project/numpy/>

**Computer Vision:**
* opencv-python 4.10.0.84 <https://pypi.org/project/opencv-python/>
* picamera2 0.3.22 <https://pypi.org/project/picamera2/>

**Robot Control:**
* picar-x 2.0.5 <https://github.com/sunfounder/picar-x/>
* robot_hat 2.2.17 <https://github.com/sunfounder/robot-hat/>

**Speech Recognition:**
* SpeechRecognition 3.11.0 <https://pypi.org/project/SpeechRecognition/>

## Installation & Manual

1. Assemble Picar-x Kit
2. Install the needed Software on the Raspberry Pi
3. Open a Terminal
4. Install the necessary libraries using pip install 
    
    Example: `pip install numpy` or `pip install -r requirements.txt` to download all needed libraries with one command
5. Go to the desired location for the repository with `cd /Path`
6. Type the command  into your terminal `git clone https://github.com/LisaSchneider99/FollowMate.git`
7. Enter the folder and run the code with `sudo python3 master.py`
8. Speak out your desired color
9. The robot will follow you

## Structure of the code

Our code is structured in such a way that, the main loops are all located in the `master.py`. This file is than accessing the necessary 
functions from different files that provide specific functionality.

For more information check the documentation

## FAQ

1. How can I change the Color for the Target?

    Simply speak the desired color when the robot is stationary.

