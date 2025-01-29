# FollowMate
Software for a robot that can follow people using foot braclet

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Member](#member)
4. [Installation & Manual](#installation--manual)
5. [Structure of the code](#Structure-of-the-code)
6. [FAQ](#faq)

## General Info


This project focuses on developing an autonomous robot capable of following a person, distinguishing between multiple individuals, and stopping when the tracked person is very close.

Such a robot can assist elderly people in navigating their homes, supermarkets, or medical facilities. It can be used to carry heavy items such as groceries or bags, making daily life easier.

The goal of this project is to create a reliable and intelligent solution for person detection and tracking, providing practical assistance in everyday situations.

## Member

| Name     | E-Mail |
| :---:        |    :----:   |
| Lisa Schneider      | lisa.schneider@smail.th-koeln.de       |
| Manuel Wette   | manuel.wette@smail.th-koeln.de        |

## Technologies

A list of technologies used within the project:

### Languages:

* Python 3.10.4 or higher <https://www.python.org/>

### Libraries:

**General:**
* numpy 2.2.2 <https://pypi.org/project/numpy/>

**Computer Vision:**
* opencv-python 4.11.0.86 <https://pypi.org/project/opencv-python/>
* picamera2 0.3.24 <https://pypi.org/project/picamera2/>

**Robot Control:**
* picar-x <https://github.com/sunfounder/picar-x/>
* robot_hat <https://github.com/sunfounder/robot-hat/>

**Speech Recognition:**
* SpeechRecognition 3.14.1 <https://pypi.org/project/SpeechRecognition/>

## Installation & Manual

1. Assamble Picar-x Kit
2. Install the needed Software on the Raspberry Pi
3. Open a Terminal
4. Install the necessary libraries using pip install 
    
    Example: `pip install pandas` or `pip install -r requirements.txt` to download all needed libraries with one command
5. Go to the desired location for the repository with `cd /Path`
6. Type the command  into your terminal `git clone https://github.com/th-koeln-optec-messsysteme/SHC_Software.git`
7. Enter the folder and run the code with `sudo python3 master.py`
8. Speak out your desired color
9. The Robot follows you around

## Structure of the code

Our code is structured in such a way that, the main loops are all located in the master.py. This file is than accessing the need 
functions from different files that provide specific functionality.

For more information check the documentation

## FAQ

1. How can I change the Color for the Target?

    Simply speak the desired color when the robot is stationary.

