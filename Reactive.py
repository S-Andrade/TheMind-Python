import threading
import time
import socket
import sys
import random

global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, playcard

def robot():
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, playcard
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
    player0_count = 0
    player1_count = 0
    targetPlayer = ""

    while True:
        #print(str(shared_dict["player0"]) + "  " + str(shared_dict["player1"]))

        if animation != "":
            message = f'PlayAnimation,player2,{animation}'
            client_socket.sendall(message.encode('utf-8'))
            print(message)
            animation = ""
        
        if speak != "":
            message = f'Speak,player2,{speak}'
            client_socket.sendall(message.encode('utf-8'))
            #print(message)
            speak = ""
            time.sleep(0.5)

        if playcard != "":
            message = f'GazeAtTarget,{playcard}'
            client_socket.sendall(message.encode('utf-8'))
            print(">" + playcard)
            time.sleep(1)
            print(">>" + playcard)
            #print(">>>>>>" + playcard)
            if playcard == "player0":
                player0_count += 1
            
            if playcard == "player1":
                player1_count += 1

            playcard = ""


        if gazetarget == "front":

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
                        player1_count += 1
                    elif currentGazeTargetFront == "player1":
                        currentGazeTargetFront = "player0"
                        player0_count += 1
                    nextTimeToLook = float(random.randrange(300,500)/100)
                    timeGaze = time.time()
                    message = f'GazeAtTarget,{currentGazeTargetFront}'
                    client_socket.sendall(message.encode('utf-8'))
                    #print(message)


        if gazetarget == "tablet":
            message = f'GazeAtTarget,tablet'
            client_socket.sendall(message.encode('utf-8'))
           

        if gazetarget == "condition":

            if  targetPlayer == "":
                print(str(player0) + "  " + str(player1))
                #MutualGaze
                if player0 == "Robot" and (player1 == "Center" or player1 == "Tablet"):
                    targetPlayer = "player0"
                    player0_count += 1
                
                elif player1 == "Robot" and (player0 == "Center" or player0 == "Tablet"):
                    targetPlayer = "player1"
                    player1_count += 1
                
                elif (player0 == "Player" and player1 == "Player") or (player0 == "Robot" and player1 == "Robot"):

                    if player0 > player1:
                        targetPlayer = "player1"
                        player1_count += 1
                    elif player1 > player0:
                        targetPlayer = "player0"
                        player0_count += 1
                    else:
                        targetPlayer = random.choice(players)

                        if targetPlayer == "player0":
                            player0_count += 1
                            
                        if targetPlayer == "player1":
                            player1_count += 1    

                #JointAttention
                elif player0 == "Player" and (player1 == "Center" or player1 == "Tablet"):
                    targetPlayer = "player1"
                    player1_count += 1
                
                elif player1 == "Player" and (player0 == "Center" or player0 == "Tablet"):
                    targetPlayer = "player0"
                    player0_count += 1

                elif player0 == "Robot" and player1 == "Player":
                    targetPlayer = "player0"
                    player0_count += 1
                
                elif player1 == "Robot" and player0 == "Player":
                    targetPlayer = "player1"
                    player1_count += 1
                
                elif player0 == "Center" and player1 == "Center":
                    targetPlayer = "mainscreen"
                
                else:
                    targetPlayer = "mainscreen"
                        
                
                nextTimeToLook = float(random.randrange(300,500)/100)
                timeGaze = time.time()
                message = f'GazeAtTarget,{targetPlayer}'
                client_socket.sendall(message.encode('utf-8'))
                print("r>" + message)

            
            if  targetPlayer != "":

                if time.time() - timeGaze >= nextTimeToLook:
                    targetPlayer = ""
                    #print(message)
                
def gaze(conn, addr, id):
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget

    print(f'Connected by {addr}')
    with conn:
        while True:
            msg = conn.recv(1024)
            if id == "player0":
                player0 = msg.decode()
            if id == "player1":
                player1 = msg.decode()

# Function to be executed in the parallel process
def worker(s, id):
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, playcard
  
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        #print(">"+msg)
        
        if "NEXTLEVEL" in msg:
            list_cards = eval(msg[9:])
            cards = list_cards[id]
            cards0 = list_cards[0]
            cards1 = list_cards[1]
            level = len(list_cards[id])
            state = "NEXTLEVEL"
            timetoplay = cards[0]
            #print(timetoplay)
        
        elif "GAMEOVER" in msg:
            if level < 10:
                animation = "sadness5"
                speak = "oh No! We lost the game!"
                gazetarget = "front"
            if level == 10:
                animation = "joy5"
                speak = "We won the game!"
                gazetarget = "front"
            time.sleep(1)
            speak = "Another game?"
            state = "GAMEOVER"

            
        
        elif "GAME" in msg:
            state = "GAME"
            starttime = time.time()
        
        elif "WELCOME" in msg:
            state = "WELCOME"

        elif "CARD" in msg:
            msgclean = msg[5:].split(",")
            player = msgclean[0]
            card = int(msgclean[1])

            if len(cards) > 0:
                    timetoplay = cards[0] - card
                    starttime = time.time()
                    if player != "2":
                        if player == 0:
                            cards0 =  [ i for i in cards0 if i!= card ] 
                        if player == 1:
                            cards1 =  [ i for i in cards1 if i!= card ]    

                        playcard = "player" + player
                        print("player" + player)
                        if timetoplay == 1:
                            speak = "My turn!"
                            gazetarget = "front"
                        #print(timetoplay)
        
        elif "LAST" in msg:
                timetoplay = 2
                starttime = time.time()
                print(timetoplay)
                last = True
        
        elif len(cards) == 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]
                cards0 = [x for x in cards0 if x > mistake]
                cards1 = [x for x in cards1 if x > mistake]

        elif len(cards) > 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]
                cards0 = [x for x in cards0 if x > mistake]
                cards1 = [x for x in cards1 if x > mistake]

                if "LAST" in msg:
                    timetoplay = 2
                    starttime = time.time()
                    print(timetoplay)
                    last = True
                else:
                    if len(cards) > 0:
                        timetoplay = cards[0] - mistake
                        starttime = time.time()
                        print(timetoplay)

            if "REFOCUS" in msg:
                state = "REFOCUS"
                
           
def main():
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, playcard

    cards = [] 
    cards0 = []
    cards1 = []
    state = "WELCOME" 
    level = 0
    lastplay = 0
    mistake = 0 
    starttime = 0 
    timetoplay = 0 
    player0 = "" 
    player1 = "" 
    speak = "" 
    animation = "" 
    gazetarget = ""
    last = False
    playcard = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('192.168.0.100', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    threading.Thread(target=worker, args=(s, 2, )).start()


    threading.Thread(target=robot).start()

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
            threading.Thread(target=gaze, args=(conn, addr, first, )).start()

    hi = False

    
    while True:
        #print(str(cards0) + " " + str(cards1) + " " + str(cards))
        if state == "WELCOME":
            #print("welcome")
            #     
            if not hi:
                speak = "Hello! I'm emis, and I will be a member of the time!"
                hi = True

                gazetarget = "front"

            s.send("WELCOME".encode())
            state = "WAITING_WELCOME"
        
        elif state == "WAITING_WELCOME":
            gazetarget = "condition"
            
        elif state == "NEXTLEVEL":
            #print("readyplay")
            if level > 1:
                falas = ["Nice! We've passed a level!", "Another level!"]
                speak = random.choice(falas)
                gazetarget = "front"
                animation = "joy1"
            else:
                gazetarget = "condition"

            s.send("READYTOPLAY".encode())
            state = "WAITING_NEXTLEVEL"

        elif state == "WAITING_NEXTLEVEL":
            gazetarget = "condition"

        elif state  == "GAME" and len(cards) > 0:
            
            gazetarget = "condition"
            
            if time.time() - starttime >= timetoplay:
                tosend = "PLAY " +  str(cards[0])
                #print(tosend)
                s.send(tosend.encode())
                lastplay = cards[0]
                cards = cards[1:]
                if len(cards) > 0:
                    timetoplay = cards[0] - lastplay
                    starttime = time.time()
                    #print(timetoplay)
                if last:
                    speak = f"I played the last card. It was a {lastplay}"
                    last = False

            elif time.time() - starttime >= timetoplay-1:
                gazetarget = "tablet"

            else:
                gazetarget = "condition"

        elif state == "MISTAKE":
            #print("mistake")
            falas = ["oh no!", "We lost a life!"]
            speak = random.choice(falas)
            gazetarget = "front"

            s.send("MISTAKE".encode())
            state = "WAITING_MISTAKE"
        
        elif state == "WAITING_MISTAKE":
            gazetarget = "condition"
        
        elif state == "REFOCUS":
            gazetarget = "condition"

            s.send("REFOCUS".encode())
            state = "WAITING_REFOCUS"
        
        elif state == "WAITING_REFOCUS":
            gazetarget = "condition"

        elif state == "GAMEOVER":
            s.send("GAMEOVER".encode())
            state = "WAITING_GAMEOVER"
            cards = []
            level = 0
            lastplay = 0
            mistake = 0
            starttime = 0
            timetoplay = 0

if __name__ == "__main__":
    main()
        