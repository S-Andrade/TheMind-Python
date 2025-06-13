import threading
import time
import socket
import sys
import random
import re
import numpy as np
import os
import logging

def setup_logger(process_name):

    directory = "8"

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the directory and log file path
    log_dir = os.path.join("logs", directory)
    log_file = os.path.join(log_dir, process_name + ".log")
    
    # Ensure the directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Create a logger
    logger = logging.getLogger(process_name)
    logger.setLevel(logging.INFO)  # Set the log level

    # Prevent duplicate handlers if logger already exists
    if not logger.handlers:
        # Create a file handler for each process based on process name
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.INFO)

        # Create a formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)
    
    return logger

global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget

def generate_gaze_time(mu, sigma, tau):
    # Generate a random value from the Gaussian distribution
    gaussian_sample = np.random.normal(mu, sigma)
    
    # Generate a random value from the Exponential distribution
    exponential_sample = np.random.exponential(tau)
    
    # Sum the two values to get the ex-Gaussian sample
    gaze_time = gaussian_sample + exponential_sample
    
    print(gaze_time/1000)
    return gaze_time / 1000

def robot():
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, targetPlayer, playcard
    
    logger = setup_logger(f"Proactive_robot")
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
    player0 = 0
    player1 = 0
    playcard_time = 0
    playcard_start = False

    while True:
        #print(str(shared_dict["player0"]) + "  " + str(shared_dict["player1"]))

        if animation != "":
            message = f'PlayAnimation,player2,{animation}'
            client_socket.sendall(message.encode('utf-8'))
            #print(message)
            animation = ""
            logger.info(f"-animation: {animation}")
        
        if speak != "":
            message = f'Speak,player2,{speak}'
            client_socket.sendall(message.encode('utf-8'))
            #print(message)
            speak = ""
            time.sleep(0.5)
            logger.info(f"-speak: {speak}")
        
        if playcard != "":
            if not playcard_start:
                message = f'GazeAtTarget,{playcard}'
                client_socket.sendall(message.encode('utf-8'))
                playcard_time = time.time()
                playcard_start = True
                logger.info(f"look at participant that played a card: {playcard}")

            if time.time() - playcard_time >= 1:
                playcard = ""
                playcard_start = False

        elif gazetarget == "front":

            currentGazeTargetCondition = ""

            if currentGazeTargetFront == "":
                currentGazeTargetFront = random.choice(players)
                nextTimeToLook = nextTimeToLook = generate_gaze_time(1206,884,1206)
                timeGaze = time.time()
                message = f'GazeAtTarget,{currentGazeTargetFront}'
                client_socket.sendall(message.encode('utf-8'))
                #print("r>" + message)
                logger.info(f"currentGazeTargetFront: {currentGazeTargetFront} -- nextTimeToLook: {nextTimeToLook}")

            elif currentGazeTargetFront != "":
                if time.time() - timeGaze >= nextTimeToLook:
                    if currentGazeTargetFront == "player0":
                        currentGazeTargetFront = "player1"
                        player1 += 1
                    elif currentGazeTargetFront == "player1":
                        currentGazeTargetFront = "player0"
                        player0 += 1
                    nextTimeToLook = generate_gaze_time(1206,884,1206)
                    timeGaze = time.time()
                    message = f'GazeAtTarget,{currentGazeTargetFront}'
                    client_socket.sendall(message.encode('utf-8'))
                    logger.info(f"currentGazeTargetFront: {currentGazeTargetFront} -- nextTimeToLook: {nextTimeToLook}")
                    #print(message)

        elif gazetarget == "tablet":
            message = f'GazeAtTarget,tablet'
            client_socket.sendall(message.encode('utf-8'))
            logger.info(f"gazeAt: tablet")

        elif gazetarget == "condition":

            if  targetPlayer == "":
            
                if len(cards0) == 0 and len(cards1) > 0:
                    targetPlayer = "player1"
                    player1 += 1
                elif len(cards1) == 0 and len(cards0) > 0:
                    targetPlayer = "player0"
                    player0 += 1
                elif player0 > player1:
                    targetPlayer = "player1"
                    player1 += 1
                elif player1 > player0:
                    targetPlayer = "player0"
                    player0 += 1
                else:
                    targetPlayer = random.choice(players)

                    if targetPlayer == "player0":
                        player0 += 1
                    
                    if targetPlayer == "player1":
                        player1 += 1
                
                gazeTime = generate_gaze_time(1206,884,1206)
                nextTimeToLook = generate_gaze_time(1510,1051,1510) + gazeTime
                timeGaze = time.time()
                endGaze = False
                message = f'GazeAtTarget,{targetPlayer}'
                client_socket.sendall(message.encode('utf-8'))
                #print("r>" + message)
                logger.info(f"targetPlayer: {targetPlayer} -- gazeTime: {gazeTime} -- nextTimeToLook: {nextTimeToLook}")

            
            if  targetPlayer != "":

                if time.time() - timeGaze >= nextTimeToLook + gazeTime:
                    targetPlayer = ""
                    #print(message)
                    logger.info(f"targetPlayer: {targetPlayer}")
                
                elif time.time() - timeGaze >= gazeTime and not endGaze:
                    message = f'GazeAtTarget,mainscreen'
                    client_socket.sendall(message.encode('utf-8'))
                    #print("mm>"+message)
                    endGaze = True

                    logger.info(f"targetPlayer: mainscreen")

# Function to be executed in the parallel process
def worker(s, id):
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, targetPlayer, playcard
  
    logger = setup_logger("worker_Proactive")
    logger.info(f"start")
    last = False
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        logger.info(f"msg -- {msg}")
        #print(">"+msg)
        print(cards)
        
        if "NEXTLEVEL" in msg:
            list_cards = eval(msg[9:])
            cards = list_cards[id]
            cards0 = list_cards[0]
            cards1 = list_cards[1]
            level = len(list_cards[id])
            state = "NEXTLEVEL"
            timetoplay = cards[0]
            logger.info(f"state: {state} -- timetoplay: {timetoplay} -- cards: {cards}")
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
            logger.info(f"state: {state} -- gazetarget: {gazetarget} -- speak: {speak}")
            
        
        elif "GAME" in msg:
            state = "GAME"
            starttime = time.time()
            logger.info(f"state: {state} -- timerestart")
        
        elif "WELCOME" in msg:
            state = "WELCOME"
            logger.info(f"state: {state}")

        elif "CARD" in msg:
            msgclean = msg[5:].split(",")
            player = msgclean[0]
            card = int(msgclean[1])
            logger.info(f"player: {player} - card: {card}")
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
                        logger.info(f"gazetarget: {gazetarget} -- speak: {speak} -- cards0: {cards0} -- cards1: {cards1}")
        
        elif "LAST" in msg:
                timetoplay = 2
                starttime = time.time()
                #print(timetoplay)
                last = True
                logger.info(f"LAST -- timetoplay: {timetoplay}")
        
        elif len(cards) == 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]
                cards0 = [x for x in cards0 if x > mistake]
                cards1 = [x for x in cards1 if x > mistake]

                logger.info(f"state: {state} -- mistake: {mistake} -- cards: {cards} -- cards0: {cards0} -- cards1: {cards1}")

        elif len(cards) > 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]
                cards0 = [x for x in cards0 if x > mistake]
                cards1 = [x for x in cards1 if x > mistake]
                logger.info(f"state: {state} -- mistake: {mistake} -- cards: {cards} -- cards0: {cards0} -- cards1: {cards1}")

                if "LAST" in msg:
                    timetoplay = 2
                    starttime = time.time()
                    #print(timetoplay)
                    last = True
                    logger.info(f"timetoplay: {timetoplay}")
                else:
                    if len(cards) > 0:
                        timetoplay = cards[0] - mistake
                        starttime = time.time()
                        logger.info(f"timetoplay: {timetoplay}")

                

            if "REFOCUS" in msg:
                state = "REFOCUS"
                logger.info(f"state: {state}")
            
def main():
    global cards, state, level, lastplay, mistake, starttime, timetoplay, player0, player1, speak, animation, gazetarget, last, cards0, cards1, targetPlayer, playcard
    logger = setup_logger("Proactive")
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
    targetPlayer = ""
    playcard = ""

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('192.168.0.104', 50001))
    msgid = "Player 2" 
    s.send(msgid.encode())

    print("conetion")
    logger.info("Connected to GameManager")



    threading.Thread(target=worker, args=(s, 2, )).start()
    logger.info("Start worker")

    threading.Thread(target=robot).start()

    tablet_time = generate_gaze_time(1192,1071,1192)

    hi = False

    before_play = False

    
    while True:
        #print(str(cards0) + " " + str(cards1) + " " + str(cards))
        if state == "WELCOME":
            #print("welcome")
            #     
            if not hi:
                speak = "Hello! I'm emis, and I will be a member of the time!"
                hi = True

                gazetarget = "front"
                logger.info(f"speak: {speak} -- gazetarget: {gazetarget}")

            
            print("hello")
            s.send("WELCOME".encode())
            state = "WAITING_WELCOME"
            logger.info(f"send: WELCOME -- state: {state}")
        
        elif state == "WAITING_WELCOME":
            gazetarget = "condition"
            logger.info(f"gazetarget: {gazetarget}")
            
        elif state == "NEXTLEVEL":
            #print("readyplay")
            if level > 1:
                falas = ["Nice! We've passed a level!", "Another level!"]
                speak = random.choice(falas)
                gazetarget = "front"
                animation = "joy1"
                logger.info(f"speak: {speak} -- gazetarget: {gazetarget}")
            else:
                gazetarget = "condition"
                logger.info(f" gazetarget: {gazetarget}")

            s.send("READYTOPLAY".encode())
            state = "WAITING_NEXTLEVEL"
            logger.info(f"send: READYTOPLAY -- state: {state}")

        elif state == "WAITING_NEXTLEVEL":
            gazetarget = "condition"
            logger.info(f"gazetarget: {gazetarget}")

        elif state  == "GAME" and len(cards) > 0:
            
            if not before_play and time.time() - starttime >= timetoplay - tablet_time:
                gazetarget = "tablet"           
                logger.info(f"gazetarget: {gazetarget}")
                before_play = True
 
            if time.time() - starttime >= timetoplay:
                tablet_time = generate_gaze_time(1192,1071,1192)
                gazetarget = "condition"
                logger.info(f"gazetarget: {gazetarget}")

                tosend = "PLAY " +  str(cards[0])
                #print(tosend)
                s.send(tosend.encode())
                lastplay = cards[0]
                cards = cards[1:]
                logger.info(f"send: {tosend} -- card: {lastplay} -- cards: {cards}")

                before_play = False

                if len(cards) > 0:
                    timetoplay = cards[0] - lastplay
                    starttime = time.time()
                    #print(timetoplay)
                    logger.info(f"timetoplay: {timetoplay}")
                if last:
                    speak = f"I played the last card. It was a {lastplay}"
                    gazetarget = "front"
                    logger.info(f"gazetarget: {gazetarget}")
                    last = False
                    logger.info(f"speak: {speak}")
            else:
                gazetarget = "condition"
                logger.info(f"gazetarget: {gazetarget}")    
        
        elif state == "MISTAKE":
            #print("mistake")
            falas = ["oh no!", "We lost a life!"]
            speak = random.choice(falas)
            gazetarget = "front"

            s.send("MISTAKE".encode())
            state = "WAITING_MISTAKE"
            logger.info(f"state: {state} -- gazetarget: {gazetarget} -- speak: {speak} -- send: MISTAKE")
        
        elif state == "WAITING_MISTAKE":
            gazetarget = "condition"
            logger.info(f"gazetarget: {gazetarget}")
        
        elif state == "REFOCUS":
            gazetarget = "condition"

            s.send("REFOCUS".encode())
            state = "WAITING_REFOCUS"
            logger.info(f"state: {state} -- gazetarget: {gazetarget} -- send: REFOCUS")
        
        elif state == "WAITING_REFOCUS":
            gazetarget = "condition"
            logger.info(f"gazetarget: {gazetarget}")

        elif state == "GAMEOVER":
            s.send("GAMEOVER".encode())
            logger.info(f"send GAMEOVER")
            state = "WAITING_GAMEOVER"
            cards = []
            level = 0
            lastplay = 0
            mistake = 0
            starttime = 0
            timetoplay = 0
            logger.info(f"state: {state} -- level: {level} -- cards: {cards}")

if __name__ == "__main__":
    main()
        