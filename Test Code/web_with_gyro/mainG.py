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
import gyro
import speechTest
import threading
import speech_recognition as sr
import Queue

try:
    IP = sys.argv[1]
except:
    IP = "192.168.1.100" #typical Baymax IP

try:
    res = sys.argv[2]
except:
    res = 1

try:
    fps = sys.argv[3]
except:
    fps = 30

r = sr.Recognizer()
q = Queue.Queue()

app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        dataZ = request.form['gyroZ']
        dataY = request.form['gyroY']
        gyro.moveHead(dataZ, dataY, IP)
        return dataZ
    else:
        return render_template('index.html')


def gen(camera,que):
    while True:
        frame = camera.get_frame()
        stringy = b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        que.put(stringy)


@app.route('/speech')
def tts():
    speechTest.recognize(IP)
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    t = threading.Thread(target=gen, args=[VideoCamera(IP, res, fps),q])
    t.start()
    return Response(q.get(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5003)
