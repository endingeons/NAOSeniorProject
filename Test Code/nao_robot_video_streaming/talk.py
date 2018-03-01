import keyboard
from naoqi import ALProxy


def keyPress(e):
    global word
    global ttsProx
    ttsProx = ALProxy("ALTextToSpeech", '192.168.1.149', 9559)
    if keyboard.is_pressed('enter'):
        ttsProx.say(str(word))
        word = ''
    elif keyboard.is_pressed('space'):
        word = word + ' '
    else:
        try:
            word = word + e.name
        except:
            word = e.name
    if keyboard.is_pressed('esc'):
        keyboard.unhook_all()


if __name__ == '__main__':
    keyboard.on_press(keyPress)
    keyboard.wait()
