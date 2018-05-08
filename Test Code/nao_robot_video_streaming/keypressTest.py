import keyboard
from naoqi import ALProxy


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


moProx = ALProxy("ALMotion", '192.168.1.100', 9559)  # sets up a proxy to robot at specified ip
moProx.setStiffnesses("Head", 1)

# binds function keyPress to keyboard events
keyboard.hook(keyPress)

# waits indefinitely for keyboard presses and control head based on arrow keys
keyboard.wait()



