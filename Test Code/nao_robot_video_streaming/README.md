# Visual and Aural Telepresence via NAO #
A 2017-2018 TCNJ senior project in which students attempt to create a remote presence using a NAO Robot with a headset made from a gaming headset and Google Cardboard. Functionality will include video and audio streaming from the robot to the user, and the user will have to ability to turn their head to control the robot's head as well as speak through the robot. This headset will be combined with an arm controller to move the rest of the robot's body.


## Programming Languages ##
- Python and Python Packages:
	- NAOqi
	- SoundFile
	- NumPY
	- Flask
	- thread
- Arudino C
- HTML5 
- JavaScript

## System Requirements ##
1. Python 2.7.x
2. NAOqi 2.4.x 


## Usage ##
1. Install Python dependencies: collections, cv2, flask, keyboard, naoqi, numpy, os, PIL, pyaudio, Queue, requests, scipy.signal, serial, sounddevice, speech_recognition, StringIO, sys, threading, time, vision_definitions
2. Connect headset (or speakers and mic) and arm controller.
3. Turn on a nao robot and note its ip.
4. Run "python main.py <res>". <res> is an optional arguement which can be used to specify the resolution (8 (worst), 7, 0, 1, 2, 3 (best))
5. Put on the arm controller.
6. Navigate the browser to the NAO webpage at the computer's ip using a smart device and enter the robot's ip in the box.
7. Put the mobile device into the google cardboard and put it on. Put on the headset after putting on the google cardboard.
8. Start the system by pressing the button on the top right of the google cardboard. Stop the system at any time by pressing the button on the arm controller and saying "Deactivate system".



## Files and Descriptions (and dependencies) ##

audio_streaming_NAO.py: Processes audio from a nao robot using SoundReceiverModule class. Once the start function is called, everything will be initialized and the sound will begin to play.
(sys, naoqi, sounddevice, numpy, Queue, pyaudio, threading, collections, scipy.signal)

camera.py: Contains VideoCamera object which establishes a camera proxy and then gets individual frames from naos camera.
(cv2, naoqi, vision_definitions, PIL, StringIO)

gyro.py: Converts degree arguments for y and z to radians and constrains angles to allowable head angle of nao then moves the nao's head.
(naoqi)

keypressTest.py: Contorls nao's head using arrow keys.
(keyboard, naoqi)

LegModule3.py: Uses data from arduino from gesture sensor to move NAO, talk, and stop system. Note that the com port specified in the script is subject to change and the script will not work without updating this value.
(naoqi, serial, speechComputer, requests)

main.py: This is the main file that brings together all other scripts. Running this will begin the web application. The computer running the script must be connected to some sort of speaker and microphone, the arm controller, and the same network as a NAO robot. The website can then be accessed at the IP of the computer.
(flask, camera, sys, gyro, threading, speech_recognition, naoqi, LegModule3, audio_streaming_NAO, PIL, StringIO)

speechComputer.py: Recognizes speech through a microphone connected to your computer and sets stop flag if the user says "deactivate system".
(speech_recognition, naoqi)

speechRecorded.py: Recognizes speech from a recorded file "testing.wav" and the nao robot says the speech recognized.
(speech_recognition, naoqi, os)

talk.py: Kepes track of characters typed and has nao say the word when user presses enter.
(keyboard, naoqi)

threadtest.py and threadTest2.py: Used to test ending threads in different scripts with a threading event.
(time, threading)



## Take a look this ##
https://www.youtube.com/watch?v=Jv-BcFOcS08