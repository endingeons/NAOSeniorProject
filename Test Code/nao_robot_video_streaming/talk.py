import keyboard
from naoqi import ALProxy


def keyPress(e):
    global word
    global ttsProx
    ttsProx = ALProxy("ALTextToSpeech", '192.168.1.100', 9559)  # create tts proxy to nao

    # nao says word typed on enter, otherwise adds typed characters to the word
    if keyboard.is_pressed('enter'):
        ttsProx.say(str(word))
        word = ''
    elif keyboard.is_pressed('space'):
        word = word + ' '
    elif keyboard.is_pressed('backspace'):
        word = word[:-1]
    elif keyboard.is_pressed('left ctrl') or keyboard.is_pressed('right ctrl') or keyboard.is_pressed('left shift') or keyboard.is_pressed('right shift') or keyboard.is_pressed('alt'):
        pass
    else:
        try:
            word = word + e.name
        except:
            word = e.name

    if keyboard.is_pressed('esc'):
        keyboard.unhook_all()


if __name__ == '__main__':
    # binds keyPress function to keyboard events
    keyboard.on_press(keyPress)
    keyboard.wait()
