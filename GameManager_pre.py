#!/usr/bin/python                                                                                                                                                                      

import socket
import multiprocessing
import random
import pygame
import time
import logging
import os
import sys
from playsound import playsound

#GameState: NEXTLEVEL, REFOCUS, GAME, MISTAKE, USESTAR, DEALCARDS
#playerState: NEXTLEVEL, READYTOPLAY

def setup_logger(process_name):
    # Define the directory and log file path
    log_dir = os.path.join("logs", sys.argv[1])
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

class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.state = "NEXTLEVEL"

def broadcast(clients, message): 
        print(message)         
        for client in clients : 
            client.send(message)

def getCards(Level):
    cards = []

    if Level == 1:
        cards.append(random.randint(1, 20))
        cards.append(random.randint(50, 60))
        cards.append(random.randint(90, 100))
        #random.shuffle(cards)

    elif Level == 2:
        while len(cards) < 5:
            next_card = random.randint(50, 100)
            if next_card not in cards:
                cards.append(next_card)

        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 3:
        while len(cards) < 7:
            next_card = random.randint(1, 100)
            if next_card not in cards:
                cards.append(next_card)
        b = True
        while b:
            c = cards[random.randint(2, 6)] + 3
            if c not in cards and c < 100:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(2, 7)] + 1
            if c not in cards  and c < 100:
                cards.insert(0, c)
                b = False

    elif Level == 4:
        cards.append(1)
        e = f = g = 0
        while len(cards) < 11:
            if e < 3:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    e += 1
            if f < 3:
                next_card = random.randint(50, 70)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 4:
                next_card = random.randint(75, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(4, 6)] + 2
            if c not in cards and c < 100:
                cards.insert(7, c)
                b = False

    elif Level == 5:
        f = g = 0
        while len(cards) < 13:
            if f < 7:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 7:
                next_card = random.randint(70, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 100:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 9)] + 5
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 6:
        f = g = 0
        while len(cards) < 18:
            if f < 9:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 9:
                next_card = random.randint(70, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1

    elif Level == 7:
        f = g = 0
        while len(cards) < 19:
            if f < 3:
                next_card = random.randint(1, 10)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 16:
                next_card = random.randint(40, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 5)] + 2
            if c not in cards and c < 100:
                cards.insert(6, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(7, 13)] + 1
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 8:
        e = f = g = 0
        while len(cards) < 24:
            if e < 8:
                next_card = random.randint(1, 20)
                if next_card not in cards:
                    cards.append(next_card)
                    e += 1
            if f < 8:
                next_card = random.randint(25, 40)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 8:
                next_card = random.randint(50, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1

    elif Level == 9:
        f = g = 0
        while len(cards) < 25:
            if f < 9:
                next_card = random.randint(1, 25)
                if next_card not in cards:
                    cards.append(next_card)
                    f += 1
            if g < 16:
                next_card = random.randint(50, 100)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(9, 16)] + 3
            if c not in cards and c < 100:
                cards.insert(17, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 8)] + 1
            if c not in cards and c < 100:
                cards.append(c)
                b = False

    elif Level == 10:
        while len(cards) < 30:
            next_card = random.randint(1, 100)
            if next_card not in cards:
                cards.append(next_card)

    # Distribute cards to each player
    hands = []
    for i in range(3):
        hand = cards[i*Level : (i + 1)*Level]
        hands.append(sorted(hand))

    return hands

def gameManager(server_socket,shared_data, shared_data_lock):
    logger = setup_logger("gameManager")
    logger.info("START")

    last = False
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    shared_data["width"] = screen_info.current_w
    shared_data["height"] = screen_info.current_h - 25
    screen = pygame.display.set_mode((shared_data["width"], shared_data["height"]))

    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35)
    sfont = pygame.font.SysFont("calibri",40)

    # Define the target position (center of the screen)
    target_pos = (shared_data["width"] // 2 - shared_data["card_width"] // 2, shared_data["height"] // 2 - shared_data["card_height"] // 2)

    # Movement speed (fraction of the distance per frame)
    speed = 0.05

    # Create card surfaces
    center_card_color = (0, 0, 255)  # Blue card in center
    moving_card_color = (255, 0, 0)  # Red moving card

    center_card_surface = pygame.Surface((shared_data["card_width"], shared_data["card_height"]))
    center_card_surface.fill(center_card_color)

    moving_card_surface = pygame.Surface((shared_data["card_width"], shared_data["card_height"]))
    moving_card_surface.fill(moving_card_color)
    clock = pygame.time.Clock()
    run = True

    while True:
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shared_data["gameState"] == "GAMEOVER" and shared_data["player0State"] == "GAMEOVER" and  shared_data["player1State"] == "GAMEOVER" and  shared_data["player2State"] == "GAMEOVER":
                    logger.info("GAMEOVER")
                    with shared_data_lock:
                        shared_data["topPile"] = 0
                        print("aqui aqui")
                        shared_data["gameState"] = "WELCOME"
                        shared_data["level"] = 1 
                        shared_data["lives"] = 3
                        shared_data["player0State"] = "WELCOME"
                        shared_data["player0Cards"] =  []
                        shared_data["player1State"] = "WELCOME"
                        shared_data["player1Cards"] = []
                        shared_data["player2State"] = "WELCOME"
                        shared_data["player2Cards"] = []

                        tosend = "WELCOME"
                        broadcast(shared_data["clients"], tosend.encode())
                        logger.info("broadcast -- WELCOME")
                        
                        print("hello")

        if shared_data["gameState"] == "WELCOME":

            screen.fill((231,84,128))

            text = font.render("LEVEL "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            p0 = sfont.render("Player0: "+ str(len(shared_data["player0Cards"])), True, (0, 0, 0))
            screen.blit(p0, (10,600))
            p1 = sfont.render("Player1: "+ str(len(shared_data["player1Cards"])), True, (0, 0, 0))
            screen.blit(p1, (10,640))
            r = sfont.render("Player2: "+ str(len(shared_data["player2Cards"])), True, (0, 0, 0))
            screen.blit(r, (10, 680))
            pygame.display.flip()
        
        elif shared_data["gameState"] == "NEXTLEVEL":
            
            screen.fill((15,170,240))

            text = font.render("LEVEL "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            p0 = sfont.render("Player0: "+ str(len(shared_data["player0Cards"])), True, (0, 0, 0))
            screen.blit(p0, (10,600))
            p1 = sfont.render("Player1: "+ str(len(shared_data["player1Cards"])), True, (0, 0, 0))
            screen.blit(p1, (10,640))
            r = sfont.render("Player2: "+ str(len(shared_data["player2Cards"])), True, (0, 0, 0))
            screen.blit(r, (10, 680))
            pygame.display.flip()
        
        elif shared_data["gameState"] == "GAME":
            if shared_data["player0State"] == "MISTAKE" or shared_data["player1State"] == "MISTAKE" or shared_data["player2State"] == "MISTAKE":
                screen.fill((223, 28, 28))
            else:
                screen.fill((255, 255, 255))

            # Draw the stationary center card
            screen.blit(center_card_surface, target_pos)
            center_card_text = font.render(str(shared_data["topPile"]), True, (255, 255, 255))
            center_card_text_rect = center_card_text.get_rect(center=(target_pos[0] + shared_data["card_width"] // 2, target_pos[1] + shared_data["card_height"] // 2))
            screen.blit(center_card_text, center_card_text_rect)

            # Display other text elements
            lives = font.render("LIVES: " + str(2), True, (0, 0, 0))
            screen.blit(lives, (10, 10))
            level = font.render("LEVEL: " + str(9), True, (0, 0, 0))
            screen.blit(level, (10, 80))
            p0 = sfont.render("Player0: " + str(1), True, (0, 0, 0))
            screen.blit(p0, (10, shared_data["height"] - 50))
            p1 = sfont.render("Player1: " + str(10), True, (0, 0, 0))
            screen.blit(p1, (shared_data["width"] - 200, shared_data["height"] - 50))
            r = sfont.render("Player2: " + str(10), True, (0, 0, 0))
            screen.blit(r, ((shared_data["width"] / 2) - 100, 15))

            # Handle card animation
            if shared_data["cardplayed"] != 0:
                with shared_data_lock:
                    # Update card position (linear interpolation)
                    shared_data["current_pos"][0] += (target_pos[0] - shared_data["current_pos"][0]) * speed
                    shared_data["current_pos"][1] += (target_pos[1] - shared_data["current_pos"][1]) * speed

                # Draw the moving card
                screen.blit(moving_card_surface, shared_data["current_pos"])
                moving_card_text = font.render(str(shared_data["cardplayed"]), True, (255, 255, 255))
                moving_card_text_rect = moving_card_text.get_rect(center=(shared_data["current_pos"][0] + shared_data["card_width"] // 2, shared_data["current_pos"][1] + shared_data["card_height"] // 2))
                screen.blit(moving_card_text, moving_card_text_rect)

                # Check if the card has reached the target position
                if abs(shared_data["current_pos"][0] - target_pos[0]) < 1 and abs(shared_data["current_pos"][1] - target_pos[1]) < 1:
                    with shared_data_lock:
                        shared_data["topPile"] = shared_data["cardplayed"]
                        shared_data["cardplayed"] = 0

            # Update the display
            pygame.display.flip()
            clock.tick(60)
                
        elif shared_data["gameState"] == "REFOCUS":
            screen.fill((51,160,44)) 
            text = font.render(str(shared_data["topPile"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            level = font.render("LEVEL: "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(level, (10,80))
            p0 = sfont.render("Player0: "+ str(len(shared_data["player0Cards"])), True, (0, 0, 0))
            screen.blit(p0, (10,600))
            p1 = sfont.render("Player1: "+ str(len(shared_data["player1Cards"])), True, (0, 0, 0))
            screen.blit(p1, (10,640))
            r = sfont.render("Player2: "+ str(len(shared_data["player2Cards"])), True, (0, 0, 0))
            screen.blit(r, (10, 680))
            pygame.display.flip()

        elif shared_data["gameState"] == "GAMEOVER":
            time.sleep(1)
            screen.fill((255,140,0)) 
            text = font.render("PLAY AGAIN?", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        if len(shared_data["player0Cards"]) == 0 and len(shared_data["player1Cards"]) == 0 and len(shared_data["player2Cards"]) == 1:

            if not last:
                logger.info("only player2 as cards")
                broadcast(shared_data["clients"], "LAST".encode())
                logger.info("broadcast -- LAST")
                last = True
        
        elif shared_data["gameState"] == "WELCOME" and  shared_data["player0State"] == "NEXTLEVEL" and  shared_data["player1State"] == "NEXTLEVEL" and  shared_data["player2State"] == "NEXTLEVEL":
            with shared_data_lock: 
                shared_data["gameState"] = "NEXTLEVEL"
                logger.info("NEXTLEVEL")
                last = False
                cards_p0, cards_p1, cards_p2 = getCards(shared_data["level"])
                shared_data["player0Cards"] = cards_p0
                shared_data["player1Cards"] = cards_p1
                shared_data["player2Cards"] = cards_p2
            cards = [cards_p0, cards_p1, cards_p2]
            tosend = "NEXTLEVEL " + str(cards)
            broadcast(shared_data["clients"], tosend.encode())
            logger.info(f"broadcast -- {tosend}")

        elif shared_data["gameState"] == "NEXTLEVEL" and  shared_data["player0State"] == "GAME" and  shared_data["player1State"] == "GAME" and  shared_data["player2State"] == "GAME":
            with shared_data_lock: 
                shared_data["gameState"] = "GAME"
            logger.info("GAME")
            broadcast(shared_data["clients"], "GAME".encode())
            logger.info("broadcast -- GAME")

        elif shared_data["gameState"] == "GAME" and  len(shared_data["player0Cards"]) == 0 and len(shared_data["player1Cards"]) == 0 and len(shared_data["player2Cards"]) == 0:
            with shared_data_lock: 
                print(shared_data["gameState"])
                shared_data["level"] += 1
            logger.info(f'level: {shared_data["level"]}')

            time.sleep(2)

            if shared_data["level"] == 5:
                with shared_data_lock: 
                    shared_data["gameState"] = "GAMEOVER"

                    time.sleep(1)
                print(">>>"+shared_data["gameState"])
                logger.info("GAMEOVER")
                broadcast(shared_data["clients"], "GAMEOVER".encode())
                logger.info("broadcast -- GAMEOVER")
            else:
                with shared_data_lock: 
                    print("aqui")
                    shared_data["gameState"] = "WELCOME"
                    shared_data["topPile"] = 0
                    shared_data["player0State"] = "WELCOME"
                    shared_data["player1State"] = "WELCOME"
                    shared_data["player2State"] = "WELCOME"
                logger.info("WELCOME")
                cards = [cards_p0, cards_p1, cards_p2]
                logger.info(f"cards: {cards}")
                tosend = "WELCOME " + str(cards)
                broadcast(shared_data["clients"], tosend.encode())
                logger.info(f"broadcast -- {tosend}")

        elif shared_data["gameState"] == "GAME" and  (len(shared_data["player0Cards"]) == 0 or shared_data["player0State"] == "MISTAKE") and  (len(shared_data["player1Cards"]) == 0 or shared_data["player1State"] == "MISTAKE") and  (len(shared_data["player2Cards"]) == 0 or shared_data["player2State"] == "MISTAKE"):
            with shared_data_lock: 
                shared_data["player0Cards"] = [x for x in shared_data["player0Cards"] if x >= shared_data["topPile"]]
                shared_data["player1Cards"] = [x for x in shared_data["player1Cards"] if x >= shared_data["topPile"]]
                shared_data["player2Cards"] = [x for x in shared_data["player2Cards"] if x >= shared_data["topPile"]]
                shared_data["gameState"] = "GAME"
                shared_data["player0State"] = "GAME"
                shared_data["player1State"] = "GAME"
                shared_data["player2State"] = "GAME"
            print("mistake")
            logger.info("end MISTAKE")
            broadcast(shared_data["clients"], "GAME".encode())
            logger.info("broadcast -- GAME")

        elif shared_data["gameState"] == "REFOCUS" and  (len(shared_data["player0Cards"]) == 0 or shared_data["player0State"] == "REFOCUS") and  (len(shared_data["player1Cards"]) == 0 or shared_data["player1State"] == "REFOCUS") and  (len(shared_data["player2Cards"]) == 0 or shared_data["player2State"] == "REFOCUS"):
            with shared_data_lock:     
                shared_data["gameState"] = "GAME"
                shared_data["player0State"] = "GAME"
                shared_data["player1State"] = "GAME"
                shared_data["player2State"] = "GAME"
            logger.info("end REFOCUS")
            broadcast(shared_data["clients"], "GAME".encode())
            logger.info("broadcast -- GAME")
        
        #print(">"+shared_data["gameState"])

def on_new_client(conn, addr, id, shared_data, shared_data_lock):
    logger = setup_logger(id)
    logger.info(f'Connected to Player {id}')
    with shared_data_lock: 
        clients = shared_data["clients"]
        clients.append(conn)
        shared_data["clients"] = clients
        logger.info("add client")
        
    with conn:
        while True:
            msg = conn.recv(1024)
            msg = msg.decode()
            logger.info(f"{id} -- message -- {msg}")
            print(str(id) + " " + msg)
            
                
            if shared_data["player"+id+"State"] == "WELCOME" and shared_data["gameState"] == "WELCOME" and msg == "WELCOME": 
                with shared_data_lock: 
                    shared_data["player"+id+"State"] = "NEXTLEVEL"
                    logger.info(f"{id} -- NEXTLEVEL")

            elif shared_data["player"+id+"State"] == "NEXTLEVEL" and shared_data["gameState"] == "NEXTLEVEL" and msg == "READYTOPLAY": 
                with shared_data_lock:  
                    shared_data["player"+id+"State"] = "GAME"
                    logger.info(f"{id} -- GAME")

            elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and "PLAY" in msg:  
                card_played = int(msg[5:])
                logger.info(f"{id} -- PLAY -- {card_played}")
                playsound("card-sound.mp3")
                if (len(shared_data["player0Cards"]) == 0 or card_played <= shared_data["player0Cards"][0]) and (len(shared_data["player1Cards"]) == 0 or card_played <= shared_data["player1Cards"][0]) and (len(shared_data["player2Cards"]) == 0 or card_played <= shared_data["player2Cards"][0]):
                    with shared_data_lock: 
                        #shared_data["topPile"] = card_played
                        shared_data["cardplayed"] = card_played
                        if id == "2":
                            start_pos = (shared_data["width"] - shared_data["card_width"], shared_data["height"])  # Right bottom corner
                        elif id == "1":
                            start_pos = (0, shared_data["height"])  # Left bottom corner
                        elif id == "0":
                            start_pos = (shared_data["width"] // 2 - shared_data["card_width"] // 2, 0)
                       
                        shared_data["current_pos"] = list(start_pos)

                        shared_data["player"+id+"Cards"] = shared_data["player"+id+"Cards"][1:]

                    sendit = f"CARD {id},{str(card_played)}"
                    broadcast(shared_data["clients"], sendit.encode())
                    logger.info(f"{id} -- broadcast -- {sendit}")
                    
                else:
                    with shared_data_lock: 
                        shared_data["lives"] -= 1
                        logger.info(f'{id} -- {shared_data["lives"]}')
                    
                    if shared_data["lives"] == 0:
                      
                        with shared_data_lock: 
                            shared_data["gameState"] = "GAMEOVER"
                        
                        logger.info(f"{id} -- GAMEOVER")
                        broadcast(shared_data["clients"], "GAMEOVER".encode())
                        logger.info(f"{id} -- broadcast -- GAMEOVER")
                    else:
                        with shared_data_lock: 
                            shared_data["topPile"] = card_played
                            shared_data["player"+id+"Cards"] = shared_data["player"+id+"Cards"][1:]
                            shared_data["player"+id+"State"] = "MISTAKE"
                        logger.info(f"{id} -- MISTAKE")
                        sendit = "MISTAKE " + str(card_played)
                        broadcast(shared_data["clients"], sendit.encode())
                        logger.info(f"{id} -- broadcast -- {sendit}")
            
            elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and msg == "MISTAKE": 
                with shared_data_lock: 
                    shared_data["player"+id+"State"] = "MISTAKE"
                    logger.info(f"{id} -- MISTAKE")
                
            elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and msg == "ASK_REFOCUS": 
                with shared_data_lock: 
                    shared_data["gameState"] = "REFOCUS"
                logger.info(f"{id} -- REFOCUS")
                broadcast(shared_data["clients"], "REFOCUS".encode())
                logger.info(f"{id} -- broadcast -- REFOCUS")

            elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "REFOCUS" and msg == "REFOCUS": 
                with shared_data_lock: 
                    shared_data["player"+id+"State"] = "REFOCUS"
                logger.info(f"{id} -- REFOCUS")
            
            elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAMEOVER" and msg == "GAMEOVER": 
                with shared_data_lock: 
                    shared_data["player"+id+"State"] = "GAMEOVER"
                logger.info(f"{id} -- GAMEOVER")


def main():
    logger = setup_logger("main")
    logger.info(f'Connected to Player {id}')

    host = '127.0.0.1'
    port = 50001


    with multiprocessing.Manager() as manager:
        shared_data = manager.dict({"topPile": 0,"gameState":"WELCOME", "level":1 ,"lives": 3, "player0State": "WELCOME", "player0Cards": [],"player1State": "WELCOME", "player1Cards": [],"player2State": "WELCOME", "player2Cards": [], "cardplayed": 0,"clients": [], "current_pos": (), "with": None, "height": None, "card_width": 100, "card_height": 150})
        shared_data_lock = manager.Lock()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen()
            logger.info(f'Server listening on {host}:{port}')

            process = multiprocessing.Process(target=gameManager, args=(server_socket,shared_data, shared_data_lock))
            process.start()
            logger.info(f'gameManager start')

   
            while True:
                conn, addr = server_socket.accept()
                first = conn.recv(1024)
                first = first.decode()
                player_id = ''.join(x for x in first if x.isdigit())
                process = multiprocessing.Process(target=on_new_client, args=(conn, addr, player_id, shared_data, shared_data_lock))
                process.start()
                logger.info(f'start {player_id}')
                conn.close()
               
if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    main()



