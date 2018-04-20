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
from flask import Flask, render_template, Response, stream_with_context
from audio_streaming_NAO import SoundReceiverModule
import sys
import pygame
import time
import naoqi
import threading
from optparse import OptionParser

try:
    IP = sys.argv[1]
except:
    IP = "192.168.1.103" #Baymax

app = Flask(__name__)



@app.route('/')
def index():
    """ Main entry point
    """
    return render_template('index_audio.html')

def gen(SoundReceiver):
    SoundReceiver.get_audio()
    # pygame.init()
    # while True:
    #     bytestream = SoundReceiver.get_audio()
    #     # print(samples)
    #     bytestream.seek(0)
    #     pygame.mixer.music.load(bytestream)
    #     pygame.mixer.music.play()
    #     time.sleep(1)
    #     # return samples


@app.route('/audio_feed', methods=['GET'])
def audio_feed():
    global myBroker
    myBroker = naoqi.ALBroker("myBroker",
                              "0.0.0.0",  # listen to anyone
                              0,  # find a free port and use it
                              IP,  # parent broker IP
                              9559)  # parent broker port

    global SoundReceiver
    SoundReceiver = SoundReceiverModule("SoundReceiver", IP, 9559)
    SoundReceiver.start()
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exits
    SoundReceiver.get_audio()

    # gen(SoundReceiver)

    # return Response(gen(SoundReceiver),
    #                  mimetype='audio/wav')

    # try:
    #     # threading.Thread(target=SoundReceiver.get_audio).start()
    #     while True:
    #         time.sleep(0.00000001)
    #         SoundReceiver.get_audio()
    # except KeyboardInterrupt:
    #     print
    #     print "Interrupted by user, shutting down"
    #     myBroker.shutdown()
    #     sys.exit(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5003)