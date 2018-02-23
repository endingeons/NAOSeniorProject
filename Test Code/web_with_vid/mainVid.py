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
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import sys
import threading
import speech_recognition as sr
from naoqi import ALProxy
import Queue
import speechTest

try:
    IP = sys.argv[1]
except:
    IP = "192.168.1.149" #typical IP

try:
    res = sys.argv[2]
except:
    res = 1

try:
    fps = sys.argv[3]
except:
    fps = 30

r = sr.Recognizer()

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/speech')
def tts():
    speechTest.recognize(IP)
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(IP, res, fps)), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5003)
