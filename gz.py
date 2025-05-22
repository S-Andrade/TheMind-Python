import threading
import socket           
import time
import sys
import random

sGaze = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
sGaze.connect(('192.168.0.105', 50009))

gazes = ["player0", "player1", "mainscreen", "tablet"]
gazes = ["Shrek", "Center", "Tablet"]

def gaze():
    i = 0
    tar = random.choice(gazes)
    starttime = time.time()
    while True:
        print(tar)
        #print(time.time() - starttime)
        if time.time() - starttime > 5:
            tar = random.choice(gazes)
            print(tar)
            starttime = time.time()
        sGaze.send(tar.encode())

        time.sleep(0.01)
        i += 1

def gaze_v2(target):
    while True:
        print(target)
        sGaze.send(target.encode())
        time.sleep(0.01)

def main():
    msgaze = "player" + str(sys.argv[1])
    sGaze.send(msgaze.encode())
    threading.Thread(target = gaze).start()
    #threading.Thread(target = gaze_v2, args=(sys.argv[2], )).start()


if __name__ == "__main__":
    main()