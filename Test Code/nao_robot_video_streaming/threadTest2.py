import time
import threading


def t(stop):
    while not stop.is_set():
        print('hello')
        time.sleep(.5)
    print('im dead')
    return
