# make sure to pip install pyaudio and speechrecognition

import speech_recognition as sr
from naoqi import ALProxy

r = sr.Recognizer()
tts = ALProxy("ALTextToSpeech", "192.168.1.100", 9559)

with sr.Microphone() as source:
    print('Say Something!')
    audio = r.listen(source)
    print('Done!')

input = r.recognize_google(audio)
print(input)
tts.say(str(input))