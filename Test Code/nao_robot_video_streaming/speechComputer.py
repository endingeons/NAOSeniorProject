import speech_recognition as sr
from naoqi import ALProxy


def recognize(ip):
    r = sr.Recognizer()
    tts = ALProxy("ALTextToSpeech", ip, 9559)  # establish tts proxy to nao

    # using the speech recognition api, listen to audio from microphone until it detects a pause
    with sr.Microphone() as source:
        print('Say Something!')
        audio = r.listen(source)
        print('Done!')

    # try to recognize audio using google speech recognition api
    try:
        input = r.recognize_google(audio)
    # if the api cant recognize speech, have the robot say something in response
    except sr.UnknownValueError:
        input = 'I am trying to say something, let me try again'

    # if the input speech is "deactivate system", set the system stop flag, otherwise says the input
    if input == 'deactivate system':
        print(input)
        tts.say('system deactivating')
        return 1
    else:
        print(input)
        tts.say(str(input))
        return 0
