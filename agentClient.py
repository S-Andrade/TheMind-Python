import multiprocessing
import time
import socket
import sys
import pygame 


# Function to be executed in the parallel process
def worker(shared_dict, shared_data_lock, s, id):
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        #print(">"+msg)
        with shared_data_lock:
            if "NEXTLEVEL" in msg:
                list_cards = eval(msg[9:])
                shared_dict["cards"] = list_cards[id]
                shared_dict["level"] = len(list_cards[id])
                shared_dict['state'] = "NEXTLEVEL"
                shared_dict['timetoplay'] = shared_dict["cards"][0]
                print(shared_dict['timetoplay'])

            if "GAMEOVER" in msg:
                shared_dict["cards"] = []
                shared_dict["state"] = "WELCOME"
                shared_dict["level"] = 0
                shared_dict["lastplay"] = 0
                shared_dict["mistake"] = 0
                shared_dict["starttime"] = 0
                shared_dict["timetoplay"] = 0
            
            
            if "GAME" in msg:
                shared_dict['state'] = "GAME"
                shared_dict["starttime"] = time.time()
            
            if "WELCOME" in msg:
                shared_dict['state'] = "WELCOME"

            if "CARD" in msg:
                msgclean = msg[4:].split(",")
                player = msgclean[0]
                card = int(msgclean[1])
                if len(shared_dict["cards"]) > 0:
                        shared_dict['timetoplay'] = shared_dict["cards"][0] - card
                        print(shared_dict['timetoplay'])
            
            if "LAST" in msg:
                    shared_dict['timetoplay'] = 0
                    print(shared_dict['timetoplay'])

            if len(shared_dict["cards"]) > 0:
                if "MISTAKE" in msg:
                    shared_dict['state'] = "MISTAKE"
                    shared_dict['mistake'] = int(msg[7:])
                    shared_dict["cards"] = [x for x in shared_dict["cards"] if x > shared_dict["mistake"]]

                    if "LAST" in msg:
                        shared_dict['timetoplay'] = 0
                        print(shared_dict['timetoplay'])
                    else:
                        if len(shared_dict["cards"]) > 0:
                            shared_dict['timetoplay'] = shared_dict["cards"][0] - shared_dict['mistake']
                            print(shared_dict['timetoplay'])

                if "REFOCUS" in msg:
                    shared_dict['state'] = "REFOCUS"
                   
            

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('127.0.0.1', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    manager = multiprocessing.Manager()
    shared_dict = manager.dict({"cards": [], "state": "WELCOME", "level" : 0, "lastplay": 0, "mistake": 0, "starttime": 0, "timetoplay": 0})
    shared_data_lock = manager.Lock()

    worker_process = multiprocessing.Process(target=worker, args=(shared_dict, shared_data_lock, s, 2, ))
    worker_process.start()
    
    while True:

        if shared_dict["state"] == "WELCOME":
            print("welcome")
            s.send("WELCOME".encode())
            shared_dict["state"] = "WAITING_WELCOME"
            
        elif shared_dict["state"] == "NEXTLEVEL":
            print("readyplay")
            s.send("READYTOPLAY".encode())
            shared_dict["state"] = "WAITING_NEXTLEVEL"

        elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) > 0:

            if time.time() - shared_dict["starttime"] >= shared_dict['timetoplay']:
                tosend = "PLAY " +  str(shared_dict["cards"][0])
                print(tosend)
                s.send(tosend.encode())
                shared_dict["lastplay"] = shared_dict["cards"][0]
                shared_dict["cards"] = shared_dict["cards"][1:]
                if len(shared_dict["cards"]) > 0:
                    shared_dict['timetoplay'] = shared_dict["cards"][0] - shared_dict["lastplay"]
                    shared_dict["starttime"] = time.time()
                    print(shared_dict['timetoplay'])
        
        elif shared_dict["state"] == "MISTAKE":
            print("mistake")
            s.send("MISTAKE".encode())
            shared_dict["state"] = "WAITING_MISTAKE"
        
        elif shared_dict["state"] == "REFOCUS":
            s.send("REFOCUS".encode())
            shared_dict["state"] = "WAITING_REFOCUS"

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
        