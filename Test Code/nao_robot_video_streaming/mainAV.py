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
import time
import naoqi
import threading
from optparse import OptionParser

try:
    IP = sys.argv[1]
except:
    IP = "192.168.1.103" #Wheatley


app = Flask(__name__)

@app.route('/')
def index():
    """ Main entry point

    """
    return render_template('index_audio.html')

def gen(pip, pport):
    myBroker = naoqi.ALBroker("myBroker",
                              "0.0.0.0",  # listen to anyone
                              0,  # find a free port and use it
                              pip,  # parent broker IP
                              pport)  # parent broker port

    global SoundReceiver
    SoundReceiver = SoundReceiverModule("SoundReceiver", pip, pport)
    SoundReceiver.start()

    def streamwav():
        def generate():
            with open("signals/song.wav", "rb") as fwav:  #Need to change TODO
                data = fwav.read(1024)
                while data:
                    yield data
                    data = fwav.read(1024)

        return Response(generate(), mimetype="audio/x-wav")

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
        pport=9559)
    (opts, args_) = parser.parse_args()
    pip = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
                              "0.0.0.0",  # listen to anyone
                              0,  # find a free port and use it
                              pip,  # parent broker IP
                              pport)  # parent broker port

    global SoundReceiver
    SoundReceiver = SoundReceiverModule("SoundReceiver", pip, pport)
    SoundReceiver.start()
    # return Response(gen(SoundReceiverModule("SoundReceiver", pip, pport)),
    #              mimetype='multipart/x-mixed-replace; boundary=wav')
    # return Response(gen(pip, pport),
    #                 mimetype='multipart/x-mixed-replace; boundary=wav')


    try:
        threading.Thread(target=SoundReceiver.get_audio).start()
        while True:
            time.sleep(0.00000001)
            # SoundReceiver.get_audio()
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True,port=5003)