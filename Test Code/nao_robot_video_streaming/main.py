#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
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

try:
    fps = sys.argv[2]
except:
    fps = 30

r = sr.Recognizer()

app = Flask(__name__)


def gen(camera):
    frame = camera.get_frame()
    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global IP
    try:
        IP = str(request.form.get('enteredIP'))
        print('IP: ' + IP)
    except:
        IP = '192.168.1.149'
        print('def')
    return render_template('startpage.html')


@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        global stopFlag
        try:
            if not stopFlag.is_set():
                print('stop flag exists')
        except NameError:
            print('make a stop flag')
            stopFlag = threading.Event()

        try:
            print(request.get_data())
            if request.get_data() == 'stopFlag=1':
                print('stop')
                stopFlag.set()
                print('stop flag is: ' + str(stopFlag.is_set()))
                return redirect(url_for('index'))
                # return render_template('index.html')

        except Exception, e:
            print(e)
            print('something')

        global vids
        vids = VideoCamera(IP, res, fps)

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
        SoundReceiver = SoundReceiverModule("SoundReceiver", IP, 9559)
        SoundReceiver.start()
        soundThread = threading.Thread(target=SoundReceiver.get_audio, args=(stopFlag,))
        soundThread.daemon = True
        soundThread.start()
    return render_template('main.html')


@app.route('/video_feed')
def video_feed():
    global stopFlag
    if not stopFlag.is_set():
        return Response(gen(vids), mimetype='multipart/x-mixed-replace; boundary=frame')

    naoImage = Image.open('return.png')
    buf = StringIO.StringIO()
    naoImage.save(buf, format='PNG')
    jpeg = buf.getvalue()
    return Response(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n', mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/process_gyro', methods=['GET', 'POST'])
def process_gyro():
    global stopFlag
    dataZ = request.form['gyroZ']
    dataY = request.form['gyroY']
    if not stopFlag.is_set():
        gyro.moveHead(dataZ, dataY, IP)
    return dataY


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5003)
