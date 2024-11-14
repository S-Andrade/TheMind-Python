import multiprocessing
import time
import socket
import sys
import random



def robot(shared_dict, shared_data_lock):
    # Cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Conecta ao servidor (mesmo IP e porta usados no C#)
    server_address = ('127.0.0.1', 8080)
    client_socket.connect(server_address)

    players = ["player0", "player1"]

    targets = ["player0", "player1", "tablet"]

    currentGazeTargetFront = ""
    currentGazeTargetCondition = ""
    nextTimeToLook = 0
    gazeTime = 0
    timeGaze = time.time()
    endGaze = False

    while True:
        #print(str(shared_dict["player0"]) + "  " + str(shared_dict["player1"]))

        if shared_dict["animation"] != "":
            message = f'PlayAnimation,player2,{shared_dict["animation"]}'
            client_socket.sendall(message.encode('utf-8'))
            print(message)
            with shared_data_lock:
                shared_dict["animation"] = ""
        
        if shared_dict["speak"] != "":
            message = f'Speak,player2,{shared_dict["speak"]}'
            client_socket.sendall(message.encode('utf-8'))
            print(message)
            with shared_data_lock:
                shared_dict["speak"] = ""
            time.sleep(0.5)

        if shared_dict["gazetarget"] == "front":

            currentGazeTargetCondition = ""

            if currentGazeTargetFront == "":
                currentGazeTargetFront = random.choice(players)
                nextTimeToLook = float(random.randrange(300,500)/100)
                timeGaze = time.time()
                message = f'GazeAtTarget,{currentGazeTargetFront}'
                client_socket.sendall(message.encode('utf-8'))
                #print("r>" + message)

            elif currentGazeTargetFront != "":
                if time.time() - timeGaze >= nextTimeToLook:
                    if currentGazeTargetFront == "player0":
                        currentGazeTargetFront = "player1"
                    elif currentGazeTargetFront == "player1":
                        currentGazeTargetFront = "player0"
                    nextTimeToLook = float(random.randrange(300,500)/100)
                    timeGaze = time.time()
                    message = f'GazeAtTarget,{currentGazeTargetFront}'
                    client_socket.sendall(message.encode('utf-8'))
                    #print(message)

           

        if shared_dict["gazetarget"] == "condition":
            currentGazeTargetFront = ""

            if  currentGazeTargetCondition == "":
                currentGazeTargetCondition = random.choice(targets)
                nextTimeToLook = float(random.randrange(300,500)/100)
                gazeTime = float(random.randrange(50,300)/100)
                timeGaze = time.time()
                endGaze = False
                message = f'GazeAtTarget,{currentGazeTargetCondition}'
                client_socket.sendall(message.encode('utf-8'))
                print("r>" + message)

            
            if  currentGazeTargetCondition != "":

                if time.time() - timeGaze >= nextTimeToLook + endGaze:
                    currentGazeTargetCondition = random.choice(targets)
                    nextTimeToLook = float(random.randrange(300,500)/100)
                    gazeTime = float(random.randrange(50,300)/100)
                    timeGaze = time.time()
                    endGaze = False
                    message = f'GazeAtTarget,{currentGazeTargetCondition}'
                    client_socket.sendall(message.encode('utf-8'))
                    #print(message)
                
                elif time.time() - timeGaze >= gazeTime and not endGaze:
                    message = f'GazeAtTarget,mainscreen'
                    client_socket.sendall(message.encode('utf-8'))
                    print("mm>"+message)
                    endGaze = True

def gaze(conn, addr, id, shared_dict, shared_data_lock):
    print(f'Connected by {addr}')
    with conn:
        while True:
            msg = conn.recv(1024)
            with shared_data_lock:
                shared_dict[id] = msg.decode()

# Function to be executed in the parallel process
def worker(shared_dict, shared_data_lock, s, id):
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        #print(">"+msg)
        
        if "NEXTLEVEL" in msg:
            list_cards = eval(msg[9:])
            with shared_data_lock:
                shared_dict["cards"] = list_cards[id]
                shared_dict["level"] = len(list_cards[id])
                shared_dict['state'] = "NEXTLEVEL"
                shared_dict['timetoplay'] = shared_dict["cards"][0]
            #print(shared_dict['timetoplay'])
        
        elif "GAMEOVER" in msg:
            if shared_dict["level"] < 10:
                with shared_data_lock:
                    shared_dict["animation"] = "sadness5"
                    shared_dict["speak"] = "oh Não! Perdemos o jogo!"
                    shared_dict["gazetarget"] = "front"
            if shared_dict["level"] == 10:
                with shared_data_lock:
                    shared_dict["animation"] = "joy5"
                    shared_dict["speak"] = "Ganhamos o jogo!"
                    shared_dict["gazetarget"] = "front"
            time.sleep(1)
            with shared_data_lock:
                shared_dict["speak"] = "Mais um jogo?"
                shared_dict["state"] = "GAMEOVER"

            
        
        elif "GAME" in msg:
            with shared_data_lock:
                shared_dict['state'] = "GAME"
                shared_dict["starttime"] = time.time()
        
        elif "WELCOME" in msg:
            with shared_data_lock:
                shared_dict['state'] = "WELCOME"

        elif "CARD" in msg:
            msgclean = msg[5:].split(",")
            player = msgclean[0]
            card = int(msgclean[1])

            if len(shared_dict["cards"]) > 0:
                    with shared_data_lock:
                        shared_dict['timetoplay'] = shared_dict["cards"][0] - card
                        shared_dict["starttime"] = time.time()
                        print(shared_dict['timetoplay'])
                        if player != "2" and shared_dict['timetoplay'] == 1:
                            shared_dict["speak"] = "Agora sou eu!"
                            shared_dict["gazetarget"] = "front"
        
        elif "LAST" in msg:
                with shared_data_lock:
                    shared_dict['timetoplay'] = 2
                    shared_dict["starttime"] = time.time()
                    print(shared_dict['timetoplay'])
        
        elif len(shared_dict["cards"]) == 0:
            if "MISTAKE" in msg:
                with shared_data_lock:
                    shared_dict['state'] = "MISTAKE"

        elif len(shared_dict["cards"]) > 0:
            if "MISTAKE" in msg:
                with shared_data_lock:
                    shared_dict['state'] = "MISTAKE"
                    shared_dict['mistake'] = int(msg[7:])
                    shared_dict["cards"] = [x for x in shared_dict["cards"] if x > shared_dict["mistake"]]

                if "LAST" in msg:
                    with shared_data_lock:
                        shared_dict['timetoplay'] = 2
                        shared_dict["starttime"] = time.time()
                        print(shared_dict['timetoplay'])
                else:
                    if len(shared_dict["cards"]) > 0:
                        with shared_data_lock:
                            shared_dict['timetoplay'] = shared_dict["cards"][0] - shared_dict['mistake']
                            shared_dict["starttime"] = time.time()
                            print(shared_dict['timetoplay'])

            if "REFOCUS" in msg:
                with shared_data_lock:
                    shared_dict['state'] = "REFOCUS"
                
        
            
def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('192.168.1.169', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    manager = multiprocessing.Manager()
    shared_dict = manager.dict({"cards": [], "state": "WELCOME", "level" : 0, "lastplay": 0, "mistake": 0, "starttime": 0, "timetoplay": 0, "player0": "", "player1": "", "speak": "", "animation":"", "gazetarget": ""})
    shared_data_lock = manager.Lock()

    worker_process = multiprocessing.Process(target=worker, args=(shared_dict, shared_data_lock, s, 2, ))
    worker_process.start()

    worker_process = multiprocessing.Process(target=robot, args=(shared_dict, shared_data_lock, ))
    worker_process.start()

    """with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
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
            worker_process.start()"""

    hi = False

    
    while True:
        #print(shared_dict["state"])
        if shared_dict["state"] == "WELCOME":
            #print("welcome")
            #     
            if not hi:
                shared_dict["speak"] = "Olá! Eu sou o émis! E serei o vosso terceiro membro da equipa!"
                hi = True

                shared_dict["gazetarget"] = "front"

            s.send("WELCOME".encode())
            shared_dict["state"] = "WAITING_WELCOME"
        
        elif shared_dict["state"] == "WAITING_WELCOME":
            shared_dict["gazetarget"] = "condition"
            
        elif shared_dict["state"] == "NEXTLEVEL":
            #print("readyplay")
            if shared_dict["level"] > 1:
                falas = ["Boa! Passamos um nivel!", "Mais um nivel!"]
                shared_dict["speak"] = random.choice(falas)
                shared_dict["gazetarget"] = "front"
                shared_dict["animation"] = "joy1"
            else:
                shared_dict["gazetarget"] = "condition"

            s.send("READYTOPLAY".encode())
            shared_dict["state"] = "WAITING_NEXTLEVEL"

        elif shared_dict["state"] == "WAITING_NEXTLEVEL":
            shared_dict["gazetarget"] = "condition"

        elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) > 0:
            
            shared_dict["gazetarget"] = "condition"
            print(">>>>" + str(time.time() - shared_dict["starttime"]))
            if time.time() - shared_dict["starttime"] >= shared_dict['timetoplay']:
                print("****"+str(time.time() - shared_dict["starttime"]))
                tosend = "PLAY " +  str(shared_dict["cards"][0])
                #print(tosend)
                s.send(tosend.encode())
                shared_dict["lastplay"] = shared_dict["cards"][0]
                shared_dict["cards"] = shared_dict["cards"][1:]
                if len(shared_dict["cards"]) > 0:
                    shared_dict['timetoplay'] = shared_dict["cards"][0] - shared_dict["lastplay"]
                    shared_dict["starttime"] = time.time()
                    print(shared_dict['timetoplay'])
        
        elif shared_dict["state"] == "MISTAKE":
            #print("mistake")
            falas = ["oh não!", "Perdemos uma vida!"]
            shared_dict["speak"] = random.choice(falas)
            shared_dict["gazetarget"] = "front"

            s.send("MISTAKE".encode())
            shared_dict["state"] = "WAITING_MISTAKE"
        
        elif shared_dict["state"] == "WAITING_MISTAKE":
            shared_dict["gazetarget"] = "condition"
        
        elif shared_dict["state"] == "REFOCUS":
            shared_dict["gazetarget"] = "condition"

            s.send("REFOCUS".encode())
            shared_dict["state"] = "WAITING_REFOCUS"
        
        elif shared_dict["state"] == "WAITING_REFOCUS":
            shared_dict["gazetarget"] = "condition"

        elif shared_dict["state"] == "GAMEOVER":
            s.send("GAMEOVER".encode())
            shared_dict["state"] = "WAITING_GAMEOVER"
            shared_dict["cards"] = []
            shared_dict["level"] = 0
            shared_dict["lastplay"] = 0
            shared_dict["mistake"] = 0
            shared_dict["starttime"] = 0
            shared_dict["timetoplay"] = 0

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
        