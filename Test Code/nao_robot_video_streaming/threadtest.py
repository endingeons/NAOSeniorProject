import time
import threading
import threadTest2


# def t(stop):
#     while not stop.is_set():
#         print('hello')
#         time.sleep(.5)
#     print('im dead')
#     return

threadkiller = threading.Event()
aThread = threading.Thread(target=threadTest2.t, args=(threadkiller,))
aThread.daemon = True
print('start it')
aThread.start()
print('time to wait')
time.sleep(10)
print('goodbye')
threadkiller.set()
print('i hope it stopped')