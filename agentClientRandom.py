import multiprocessing
import time
import socket
import sys


def robot(shared_dict, shared_data_lock):
    while True:
        print(str(shared_dict["player0"]) + "  " + str(shared_dict["player1"]))
    #pass

def gaze(conn, addr, id, shared_dict, shared_data_lock):
    print(f'Connected by {addr}')
    with conn:
        while True:
            msg = conn.recv(1024)
            with shared_data_lock:
                shared_dict[id] = msg

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
                #print(shared_dict['timetoplay'])
            
            elif "GAMEOVER" in msg:
                shared_dict['state'] = "GAMEOVER"
                shared_dict["cards"] = []
                shared_dict["state"] = "WELCOME"
                shared_dict["level"] = 0
                shared_dict["lastplay"] = 0
                shared_dict["mistake"] = 0
                shared_dict["starttime"] = 0
                shared_dict["timetoplay"] = 0

            
            elif "GAME" in msg:
                shared_dict['state'] = "GAME"
                shared_dict["starttime"] = time.time()
            
            elif "WELCOME" in msg:
                shared_dict['state'] = "WELCOME"

            elif "CARD" in msg:
                card = int(msg[4:])
                if len(shared_dict["cards"]) > 0:
                        shared_dict['timetoplay'] = shared_dict["cards"][0] - card
                        print(shared_dict['timetoplay'])
            
            elif "LAST" in msg:
                    shared_dict['timetoplay'] = 0
                    print(shared_dict['timetoplay'])

            elif len(shared_dict["cards"]) > 0:
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
                   
            
            
def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('127.0.0.1', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    manager = multiprocessing.Manager()
    shared_dict = manager.dict({"cards": [], "state": "WELCOME", "level" : 0, "lastplay": 0, "mistake": 0, "starttime": 0, "timetoplay": 0, "player0": "", "player1": ""})
    shared_data_lock = manager.Lock()

    worker_process = multiprocessing.Process(target=worker, args=(shared_dict, shared_data_lock, s, 2, ))
    worker_process.start()

    worker_process = multiprocessing.Process(target=robot, args=(shared_dict, shared_data_lock, ))
    worker_process.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(("127.0.0.1", 50009))
            server_socket.listen()
            print(f'Server listening')
        except Exception as e:
            raise

        for i in range(2):
            conn, addr = server_socket.accept()
            first = conn.recv(1024)
            first = first.decode()
            worker_process = multiprocessing.Process(target=gaze, args=(conn, addr, first, shared_dict, shared_data_lock))
            worker_process.start()

    
    while True:
        #print(shared_dict["state"])
        if shared_dict["state"] == "WELCOME":
            #print("welcome")
            s.send("WELCOME".encode())
            shared_dict["state"] = "WAITING_WELCOME"
            
        elif shared_dict["state"] == "NEXTLEVEL":
            #print("readyplay")
            s.send("READYTOPLAY".encode())
            shared_dict["state"] = "WAITING_NEXTLEVEL"

        elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) > 0:

            if time.time() - shared_dict["starttime"] >= shared_dict['timetoplay']:
                tosend = "PLAY " +  str(shared_dict["cards"][0])
                #print(tosend)
                s.send(tosend.encode())
                shared_dict["lastplay"] = shared_dict["cards"][0]
                shared_dict["cards"] = shared_dict["cards"][1:]
                if len(shared_dict["cards"]) > 0:
                    shared_dict['timetoplay'] = shared_dict["cards"][0] - shared_dict["lastplay"]
                    shared_dict["starttime"] = time.time()
                    print(shared_dict['timetoplay'])
        
        if shared_dict["state"] == "MISTAKE":
            #print("mistake")
            s.send("MISTAKE".encode())
            shared_dict["state"] = "WAITING_MISTAKE"

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
        