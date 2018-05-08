#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Modified by Chelsea Cantone, Theresa Pham, and Daniel Ponsini
# Description: Modified to receive images from NAO robot instead of webcam, added gyro
# processing, added audio streaming, and styled pages to give system a better flow

from flask import Flask, render_template, Response, request, redirect, url_for
from camera import VideoCamera
import sys
import gyro
import threading
import speech_recognition as sr
import naoqi
import LegModule3
from audio_streaming_NAO import SoundReceiverModule
from PIL import Image
import StringIO


try:
    res = sys.argv[1]
except:
    res = '1'

fps = 30

r = sr.Recognizer()

app = Flask(__name__)


# generator function for getting camera frames from the nao robot
def gen(camera):
    frame = camera.get_frame()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# defines the home page
@app.route('/', methods=['POST', 'GET'])
def index():
    global stopFlag
    # checks if the stop flag exists and clears it to reset the system if it does exist
    try:
        if stopFlag.is_set():
            print('stop flag exists')
            stopFlag.clear()
    except NameError:
        print('no stopflag yet')
    return render_template('index.html')


# defines the intermediate start page
@app.route('/start', methods=['POST'])
def start():
    global IP
    # gets the IP from the form submitted on the previous page (or sets it to a default)
    try:
        IP = str(request.form.get('enteredIP'))
        print('IP: ' + IP)
    except:
        IP = '192.168.1.149'
        print('def')
    return render_template('startpage.html')


# defines the main page
@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        global stopFlag
        # creates a stop flag if it doesnt exist to communicate between threads
        try:
            if not stopFlag.is_set():
                print('stop flag exists')
        except NameError:
            print('make a stop flag')
            stopFlag = threading.Event()

        # checks if the stop flag is being set by the speech thread and updates accordingly
        try:
            print(request.get_data())
            if request.get_data() == 'stopFlag=1':
                print('stop')
                stopFlag.set()
                print('stop flag is: ' + str(stopFlag.is_set()))
                return render_template('main.html')

        except Exception, e:
            print(e)
            print('something')

        global vids
        # initializes the video camera object
        vids = VideoCamera(IP, res, fps)

        # begins a new thread to handle the leg motion and talking of the nao
        legtalkthread = threading.Thread(target=LegModule3.legsAndTalk, args=(IP,))
        legtalkthread.daemon = True
        legtalkthread.start()

        global myBroker
        # We need this broker to be able to construct
        # NAOqi modules and subscribe to other modules
        # The broker must stay alive until the program exits
        myBroker = naoqi.ALBroker("myBroker",
                                  "0.0.0.0",  # listen to anyone
                                  0,  # find a free port and use it
                                  IP,  # parent broker IP
                                  9559)  # parent broker port

        global SoundReceiver
        # creates the sound receiver
        try:
            SoundReceiver = SoundReceiverModule("SoundReceiver", IP, 9559)
        except Exception, e:
            print(e)
            pass
        # begins a new thread for processing and playing the sound received from the robot
        SoundReceiver.start()
        soundThread = threading.Thread(target=SoundReceiver.get_audio, args=(stopFlag,))
        soundThread.daemon = True
        soundThread.start()
    return render_template('main.html')


# defines the source page of the video
@app.route('/video_feed')
def video_feed():
    global stopFlag
    # if the stop flag hasnt been set, get the video frame from the generator
    if not stopFlag.is_set():
        return Response(gen(vids), mimetype='multipart/x-mixed-replace; boundary=frame')

    # if the stop flag has been set, use the static image file with instructions to the user on how to return
    naoImage = Image.open('return.png')
    buf = StringIO.StringIO()
    naoImage.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return Response(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


# defines a page to process gyro data to control naos head
@app.route('/process_gyro', methods=['GET', 'POST'])
def process_gyro():
    global stopFlag
    # get the data that has been submitted through a form
    dataZ = request.form['gyroZ']
    dataY = request.form['gyroY']
    # move the head if the stop flag has not been set
    if not stopFlag.is_set():
        gyro.moveHead(dataZ, dataY, IP)
    return dataY


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)
