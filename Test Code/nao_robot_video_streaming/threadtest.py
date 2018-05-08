import time
import threading
import threadTest2


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