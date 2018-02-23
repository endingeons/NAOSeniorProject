# make sure to pip install pyaudio and speechrecognition

import speech_recognition as sr

from naoqi import ALProxy
from os import path

def recognize():
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "testing.wav")
    r = sr.Recognizer()
    tts = ALProxy("ALTextToSpeech", "192.168.1.100", 9559)

    with sr.AudioFile(AUDIO_FILE) as source:
        print('Reading...')
        audio = r.record(source)
        print('Done!')

    try:
        input = r.recognize_google(audio)
        print("NAO says:" + input)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    tts.say(str(input))

recognize()