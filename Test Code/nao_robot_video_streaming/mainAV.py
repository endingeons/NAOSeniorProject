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
from flask import Flask, render_template, Response
from audio_streaming_NAO import SoundReceiverModule
import sys
import naoqi
import time
#import pyaudio
from optparse import OptionParser

IP = sys.argv[1]

app = Flask(__name__)

@app.route('/')
def index():
    """ Main entry point

    """
    return render_template('index.html')

#def gen(camera0):
#    while True:
#        frame = camera0.get_frame()
#        yield (b'--frame\r\n'
#               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(VideoCamera(IP)),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(SoundReceiver):
    SoundReceiver.start()
    while True:
        #yield("/Users/cantonc1/Documents/test/out.ogg")
        yield("../ACDC_-_Back_In_Black-sample.ogg")

@app.route('/audio_feed')
def audio_feed():
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=IP,
        pport=5003)

    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    # myBroker = naoqi.ALBroker("myBroker",
    #    "0.0.0.0",   # listen to anyone
    #    0,           # find a free port and use it
    #    pip,         # parent broker IP
    #    pport)       # parent broker port
    #
    # Warning: SoundReceiver must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global SoundReceiver
    SoundReceiver = SoundReceiverModule(pip, pport)
    # SoundReceiver.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

    return "Hello"
    # #audio = pyaudio.PyAudio()
    # #stream = audio.open(
    # #    format=pyaudio.paInt16,
    # #    channels=AUDIO['channels'], rate=AUDIO['rate'],
    # #    input=True, output=True, stream_callback=on_audio_ready) # TODO: what stream_callback?
    #
    #
    # try:
    #     return Response(gen(SoundReceiverModule("SoundReceiver", pip)),
    #                     mimetype='audio/ogg')

    # SoundReceiver.start()
    # #SoundReceiver.aSoundDataInterlaced[0]
    #
    # # except KeyboardInterrupt:
    # #     print
    # #     print "Interrupted by user, shutting down"
    # #     sys.exit(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5003)
