from naoqi import ALProxy
import serial
import speechComputer
import requests

# Movement is in meters, Rotation is in radians
# Positive values are forward/left/c-clkwise
# Negative values are backward/right/clkwise


def legsAndTalk(ip):
    NAO_IP = ip
    NAO_Port = 9559

    # Attempt to create proxy object from ALMotion Module from Naoqi OS
    try:
        motion = ALProxy("ALMotion", NAO_IP, NAO_Port)  # (Module, Robot, Robot Port)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    # Attempt to create proxy object from ALTextToSpeech Module from Naoqi OS
    try:
        tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_Port)  # (Module, Robot, Robot Port)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    # Attempt to create proxy object from ALRobotPosture Module from Naoqi OS
    try:
        posture = ALProxy("ALRobotPosture", NAO_IP, NAO_Port)  # (Module, Robot, Robot Port)
    except Exception, e:
        print "Could not create proxy to ALMemory"
        print "Error was: ", e

    # Make NAO stand up
    posture.goToPosture("StandInit", 1.0)

    # Arduino Setup
    port = 'COM4'  # Subject to change
    baudrate = 9600

    arduino = serial.Serial(port, baudrate)

    try:
        while True:
            data = arduino.readline()[:-2]
            if data:
                # Move 1 meter
                if data == "f":
                    print data
                    motion.post.moveTo(1.0, 0, 0)
                    # tts.say("Forward")

                elif data == "b":
                    print data
                    motion.post.moveTo(-1.0, 0, 0)
                    # tts.say("Backward")

                elif data == "l":
                    print data
                    motion.post.moveTo(0, 1.0, 0)
                    # tts.say("Left")

                elif data == "r":
                    print data
                    motion.post.moveTo(0, -1.0, 0)
                    # tts.say("Right")

                # Cancel action
                elif data == "s":
                    print data
                    motion.post.stopMove()
                    # tts.say("Stop")

                # Rotate 45 degrees
                elif data == "c":
                    print data
                    motion.post.moveTo(0, 0, -0.79)
                    # tts.say("Clockwise")

                elif data == "k":
                    print data
                    motion.post.moveTo(0, 0, 0.79)
                    # tts.say("Counter Clockwise")

                elif data == "push":
                    print data
                    stop = speechComputer.recognize(NAO_IP)
                    if stop == 1:
                        posture.goToPosture("Crouch", 1.0)
                        motion.setStiffnesses("Body", 0.0)
                        requests.post("http://192.168.1.101:5003/main", data={'stopFlag': 1})
                        break

    except KeyboardInterrupt:
        posture.goToPosture("Crouch", 1.0)
        motion.setStiffnesses("Body", 0.0)
