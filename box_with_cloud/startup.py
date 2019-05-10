import time
from threading import Thread
import os

def startprgm(i):
    print "Running thread %d" % i
    if (i == 0):
        time.sleep(1)
        print('Running: logger')
        os.system("sudo python /home/pi/Desktop/box/myappy.py")
    elif (i == 1):
        time.sleep(3)
        print('Running: Server')
        os.system("sudo python /home/pi/Desktop/box/server.py")
    else:
        pass

for i in range(2):
    t = Thread(target=startprgm, args=(i,))
    t.start()
	
	
print("System Online")
