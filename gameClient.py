
import socket           
import time

import sys
import time
import zmq
import joblib
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
s.connect(('127.0.0.1', 50001))

"""first = s.recv(1024)
        first = first.decode()
        print(first)"""

def playingTheMind():
    cards = []
    state =  "NEXTLEVEL"
    while True:
        print(state)
        if state == "NEXTLEVEL":
            #msg = s.recv(1024)
            #msg = msg.decode()
            #print(msg)
            input("NextLevel>")
            s.send("READYTOPLAY".encode())
            cards = s.recv(1024)
            cards = cards.decode()
            cards = eval(cards)
            print(cards)
            state = "REFOCUS"
            msg = s.recv(1024)
            msg = msg.decode()
            print(msg)

        elif state == "REFOCUS":
            input("Refocus>")
            s.send("REFOCUS".encode())
            state = "GAME"
            msg = s.recv(1024)
            msg = msg.decode()
            print(msg)

        elif state == "GAME" and len(cards) > 0:
            while len(cards) > 0:
                
                input(f"PlayCard {cards[0]} >")
                s.send(str(cards[0]).encode())
                cards.pop(0)

        elif state == "GAME" and len(cards) == 0:
            msg = s.recv(1024)
            msg = msg.decode()
            print(msg)
            state = "NEXTLEVEL"

        

        
def main():
    msgid = "Player " + str(sys.argv[1])
    s.send(msgid.encode())
    threading.Thread(target = playingTheMind).start()
   

if __name__ == "__main__":
    main()
