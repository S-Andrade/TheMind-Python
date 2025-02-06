import threading
import time
import socket
import sys
import random

global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget


def robot():
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget

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

        if animation != "":
            message = f'PlayAnimation,player2,{animation}'
            client_socket.sendall(message.encode('utf-8'))
            print(message)
            animation = ""
        
        if speak != "":
            message = f'Speak,player2,{speak}'
            client_socket.sendall(message.encode('utf-8'))
            print(message)
            speak = ""
            time.sleep(0.5)

        if gazetarget == "front":

            currentGazeTargetCondition = ""

            if currentGazeTargetFront == "":
                currentGazeTargetFront = random.choice(players)
                nextTimeToLook = float(random.randrange(900,1400)/100)
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
                    nextTimeToLook = float(random.randrange(900,1400)/100)
                    timeGaze = time.time()
                    message = f'GazeAtTarget,{currentGazeTargetFront}'
                    client_socket.sendall(message.encode('utf-8'))
                    #print(message)

           

        if gazetarget == "condition":
            currentGazeTargetFront = ""

            if  currentGazeTargetCondition == "":
                currentGazeTargetCondition = random.choice(targets)
                gazeTime = float(random.randrange(50,300)/100)
                nextTimeToLook = float(random.randrange(900,1400)/100) + gazeTime
                timeGaze = time.time()
                endGaze = False
                message = f'GazeAtTarget,{currentGazeTargetCondition}'
                client_socket.sendall(message.encode('utf-8'))
                #print("r>" + message)

            
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
                    #print("mm>"+message)
                    endGaze = True

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
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last

    last = False

    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        #print(">"+msg)
        
        if "NEXTLEVEL" in msg:
            list_cards = eval(msg[9:])
            cards = list_cards[id]
            level = len(list_cards[id])
            state = "NEXTLEVEL"
            timetoplay = cards[0]
            #print(timetoplay)
        
        elif "GAMEOVER" in msg:
            if level < 10:
                animation = "sadness5"
                speak = "oh Não! Perdemos o jogo!"
                gazetarget = "front"
            if level == 10:
                animation = "joy5"
                speak = "Ganhamos o jogo!"
                gazetarget = "front"
            time.sleep(1)
            speak = "Mais um jogo?"
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
                    print(timetoplay)
                    if player != "2" and timetoplay == 1:
                        speak = "Agora sou eu!"
                        gazetarget = "front"
        
        elif "LAST" in msg:
                timetoplay = 2
                starttime = time.time()
                print(timetoplay)
                last = True
        
        elif len(cards) == 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"

        elif len(cards) > 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]

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
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last

    cards = [] 
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


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('192.168.1.169', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    print("conetion")



    threading.Thread(target=worker, args=(s, 2, )).start()

    threading.Thread(target=robot).start()


    hi = False

    
    while True:
        #print(state)
        if state == "WELCOME":
            #print("welcome")
            #     
            if not hi:
                speak = "Olá! Eu sou o émis! E serei o vosso terceiro membro da equipa!"
                hi = True

                gazetarget = "front"

            s.send("WELCOME".encode())
            state = "WAITING_WELCOME"
        
        elif state == "WAITING_WELCOME":
            gazetarget = "condition"
            
        elif state == "NEXTLEVEL":
            #print("readyplay")
            if level > 1:
                falas = ["Boa! Passamos um nivel!", "Mais um nivel!"]
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
            print(">>>>" + str(time.time() - starttime))
            if time.time() - starttime >= timetoplay:
                print("****"+str(time.time() - starttime))
                tosend = "PLAY " +  str(cards[0])
                #print(tosend)
                s.send(tosend.encode())
                lastplay = cards[0]
                cards = cards[1:]
                if len(cards) > 0:
                    timetoplay = cards[0] - lastplay
                    starttime = time.time()
                    print(timetoplay)
                if last:
                    speak = f"Joguei a ultima carta. Era um {lastplay}"
                    last = False
                
        
        elif state == "MISTAKE":
            #print("mistake")
            falas = ["oh não!", "Perdemos uma vida!"]
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
        