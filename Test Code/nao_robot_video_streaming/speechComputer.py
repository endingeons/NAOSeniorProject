# make sure to pip install pyaudio and speechrecognition

import speech_recognition as sr
from naoqi import ALProxy

def recognize(ip):
    r = sr.Recognizer()
    tts = ALProxy("ALTextToSpeech", ip, 9559)

    with sr.Microphone() as source:
        print('Say Something!')
        audio = r.listen(source)
        print('Done!')

    try:
        input = r.recognize_google(audio)
    except UnknownValueError:
        input = 'I didnt catch that'
    print(input)
    tts.say(str(input))