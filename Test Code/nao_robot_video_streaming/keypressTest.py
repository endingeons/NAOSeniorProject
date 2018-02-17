import keyboard
import time
from naoqi import ALProxy
import pyautogui, sys

def keyPress(e):
    if keyboard.is_pressed('up'):
        print('up')
        names = "HeadPitch"
        changes = -0.1
        fracSpeed = 0.1
        moProx.changeAngles(names, changes, fracSpeed)
    elif keyboard.is_pressed('down'):
        print('down')
        names = "HeadPitch"
        changes = 0.1
        fracSpeed = 0.1
        moProx.changeAngles(names, changes, fracSpeed)
    elif keyboard.is_pressed('right'):
        print('right')
        names = "HeadYaw"
        changes = -0.1
        fracSpeed = 0.1
        moProx.changeAngles(names, changes, fracSpeed)
    elif keyboard.is_pressed('left'):
        print('left')
        names = "HeadYaw"
        changes = 0.1
        fracSpeed = 0.1
        moProx.changeAngles(names, changes, fracSpeed)
    elif keyboard.is_pressed('esc'):
        keyboard.unhook_all()
        moProx.setStiffnesses("Head", 0.0)


moProx = ALProxy("ALMotion", '192.168.1.149', 9559)
moProx.setStiffnesses("Head", 1)

keyboard.hook(keyPress)
keyboard.wait()



