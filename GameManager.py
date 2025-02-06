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
import threading


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
        self.state = "WELCOME"
    
    def print_player(self):
        print(str(self.id) + " " + str(self.state) + " " + str(self.cards))

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

global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 


def gameManager(server_socket):
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 
    logger = setup_logger("gameManager")
    logger.info("START")

    last = False
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 25
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35)
    sfont = pygame.font.SysFont("calibri",40)

    image = pygame.image.load("arrow.png").convert_alpha()
    image = pygame.transform.scale(image, (150, 150))

   
    run = True

    while run:
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameState == "GAMEOVER" and p0.state == "GAMEOVER" and  p1.state == "GAMEOVER" and  p2.state == "GAMEOVER":
                    logger.info("GAMEOVER")
                    topPile = 0
                    gameState = "WELCOME"
                    level = 1 
                    lives = 3
                    p0.state = "WELCOME"
                    p0.cards =  []
                    p1.state = "WELCOME"
                    p1.cards = []
                    p2.state = "WELCOME"
                    p2.cards = []

                    tosend = "WELCOME"
                    broadcast(clients, tosend.encode())
                    logger.info("broadcast -- WELCOME")

        #p0.print_player()
        #p1.print_player()
        #p2.print_player()

        if len(p0.cards) == 0 and len(p1.cards) == 0 and len(p2.cards) == 1:

            if not last:
                logger.info("only player2 as cards")
                broadcast(clients, "LAST".encode())
                logger.info("broadcast -- LAST")
                last = True
        
        elif gameState == "WELCOME" and  p0.state == "NEXTLEVEL" and  p1.state == "NEXTLEVEL" and  p2.state == "NEXTLEVEL":
            gameState = "NEXTLEVEL"
            logger.info("NEXTLEVEL")
            last = False
            cards_p0, cards_p1, cards_p2 = getCards(level)
            p0.cards = cards_p0
            p1.cards = cards_p1
            p2.cards = cards_p2
            cards = [cards_p0, cards_p1, cards_p2]
            tosend = "NEXTLEVEL " + str(cards)
            broadcast(clients, tosend.encode())
            logger.info(f"broadcast -- {tosend}")

        elif gameState == "NEXTLEVEL" and  p0.state == "GAME" and  p1.state == "GAME" and  p2.state == "GAME":
            gameState = "GAME"
            logger.info("GAME")
            broadcast(clients, "GAME".encode())
            logger.info("broadcast -- GAME")

        elif gameState == "GAME" and  len(p0.cards) == 0 and len(p1.cards) == 0 and len(p2.cards) == 0:
            level += 1
            logger.info(f'level: {level}')

            time.sleep(2)

            if level == 5:
                gameState = "GAMEOVER"

                time.sleep(1)
                
                logger.info("GAMEOVER")
                broadcast(clients, "GAMEOVER".encode())
                logger.info("broadcast -- GAMEOVER")
            else:
                gameState = "WELCOME"
                topPile = 0
                p0.state = "WELCOME"
                p1.state = "WELCOME"
                p2.state = "WELCOME"
                logger.info("WELCOME")
                cards = [cards_p0, cards_p1, cards_p2]
                logger.info(f"cards: {cards}")
                tosend = "WELCOME " + str(cards)
                broadcast(clients, tosend.encode())
                logger.info(f"broadcast -- {tosend}")

        elif gameState == "GAME" and  (len(p0.cards) == 0 or p0.state == "MISTAKE") and  (len(p1.cards) == 0 or p1.state == "MISTAKE") and  (len(p2.cards) == 0 or p2.state == "MISTAKE"):
            p0.cards = [x for x in p0.cards if x >= topPile]
            p1.cards = [x for x in p1.cards if x >= topPile]
            p2.cards = [x for x in p1.cards if x >= topPile]
            gameState = "GAME"
            p0.state = "GAME"
            p1.state = "GAME"
            p2.state = "GAME"
            print("mistake")
            logger.info("end MISTAKE")
            broadcast(clients, "GAME".encode())
            logger.info("broadcast -- GAME")

        elif gameState == "GAME" and (p0.state == "REFOCUS" or p1.state == "REFOCUS" or p1.state == "REFOCUS"):
            gameState = "REFOCUS"
            logger.info("REFOCUS")

        elif gameState == "REFOCUS" and  (len(p0.cards) == 0 or p0.state == "REFOCUS") and  (len(p1.cards) == 0 or p1.state == "REFOCUS") and  (len(p2.cards) == 0 or p2.state == "REFOCUS"):
            gameState = "GAME"
            p0.state = "GAME"
            p1.state = "GAME"
            p2.state = "GAME"
            logger.info("end REFOCUS")
            broadcast(clients, "GAME".encode())
            logger.info("broadcast -- GAME")
        

        if gameState == "WELCOME":

            screen.fill((231,84,128))

            text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = font.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0 = sfont.render("Player0: "+ str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl0, (10, height-50))
            pl1 = sfont.render("Player1: "+ str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl1, (width-200,height-50))
            r = sfont.render("Player2: "+ str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(r, (width/2-50, 10))
            pygame.display.flip()
        
        elif gameState == "NEXTLEVEL":
            
            screen.fill((15,170,240))

            text = font.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = font.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0 = sfont.render("Player0: "+ str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl0, (10, height-50))
            pl1 = sfont.render("Player1: "+ str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl1, (width-200,height-50))
            r = sfont.render("Player2: "+ str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(r, (width/2-50, 10))
            pygame.display.flip()
        
        elif gameState == "GAME":
            if p0.state == "MISTAKE" or p1.state == "MISTAKE" or p1.state == "MISTAKE":
                screen.fill((223, 28, 28))
            else:
                screen.fill((255, 255, 255))
            
            text = font.render(str(topPile), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = font.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            lev = font.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(lev, (10,80))
            pl0 = sfont.render("Player0: "+ str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl0, (10, height-50))
            pl1 = sfont.render("Player1: "+ str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl1, (width-200,height-50))
            r = sfont.render("Player2: "+ str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(r, (width/2-50, 10))

            

            if len(player_played) > 0 and time.time() - player_played[1] < 2:
            
                if player_played[0] == "0":
                    print(player_played)
                    angle = 45
                    rotated_image = pygame.transform.rotate(image, angle)
                    rect = rotated_image.get_rect(center=(width/4, height*(3/4)))
                    screen.blit(rotated_image, rect.topleft)

                if player_played[0] == "1":
                    angle = 135
                    rotated_image = pygame.transform.rotate(image, angle)
                    rect = rotated_image.get_rect(center=(width*(3/4), height*(3/4)))
                    screen.blit(rotated_image, rect.topleft)
                    
                if player_played[0] == "2":
                    angle = -90
                    rotated_image = pygame.transform.rotate(image, angle)
                    rect = rotated_image.get_rect(center=(width/2, height/4))
                    screen.blit(rotated_image, rect.topleft)
            
            pygame.display.flip()
                

            
                    
        elif gameState == "REFOCUS":
            screen.fill((51,160,44)) 
            text = font.render(str(topPile), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = font.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            lev = font.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(lev, (10,80))
            pl0 = sfont.render("Player0: "+ str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl0, (10, height-50))
            pl1 = sfont.render("Player1: "+ str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl1, (width-200,height-50))
            r = sfont.render("Player2: "+ str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(r, (width/2-50, 10))
            pygame.display.flip()

        elif gameState == "GAMEOVER":
            time.sleep(1)
            screen.fill((255,140,0)) 
            text = font.render("PLAY AGAIN?", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()


def on_new_client(conn, addr, id):
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 

    logger = setup_logger(id)
    logger.info(f'Connected to Player {id}')
    
    clients.append(conn)

    with conn:
        while True:
            msg = conn.recv(1024)
            msg = msg.decode()
            logger.info(f"{id} -- message -- {msg}")
            print(str(id) + " " + msg)
            
            if ((id == "0" and p0.state == "WELCOME") or (id == "1" and p1.state == "WELCOME")  or (id == "2" and p2.state == "WELCOME")) and gameState == "WELCOME" and msg == "WELCOME":   
                if id == "0":
                    p0.state = "NEXTLEVEL"
                if id == "1":
                    p1.state = "NEXTLEVEL"
                if id == "2":
                    p2.state = "NEXTLEVEL"
                logger.info(f"{id} -- NEXTLEVEL")

            elif ((id == "0" and p0.state == "NEXTLEVEL") or (id == "1" and p1.state == "NEXTLEVEL")  or (id == "2" and p2.state == "NEXTLEVEL")) and gameState == "NEXTLEVEL" and msg == "READYTOPLAY":   
                if id == "0":
                    p0.state = "GAME"
                if id == "1":
                    p1.state = "GAME"
                if id == "2":
                    p2.state = "GAME"
                logger.info(f"{id} -- GAME")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAME" and "PLAY" in msg:   
             
                card_played = int(msg[5:])
                topPile = card_played
                player_played = [id , time.time()] 
                logger.info(f"{id} -- PLAY -- {card_played}")
                playsound("card-sound.mp3")


                if (len(p0.cards) == 0 or card_played <= p0.cards[0]) and (len(p1.cards) == 0 or card_played <= p1.cards[0]) and (len(p2.cards) == 0 or card_played <= p2.cards[0]):
                    
                    if id == "0":
                        p0.cards = p0.cards[1:]
                    if id == "1":
                        p1.cards = p1.cards[1:]
                    if id == "2":
                        p2.cards = p2.cards[1:]

                    sendit = f"CARD {id},{str(card_played)}"
                    broadcast(clients, sendit.encode())
                    logger.info(f"{id} -- broadcast -- {sendit}")
                    
                else:
                    lives -= 1
                    logger.info(f'{id} -- {lives}')
                    
                    if lives == 0:
                        gameState = "GAMEOVER"
                        logger.info(f"{id} -- GAMEOVER")
                        broadcast(clients, "GAMEOVER".encode())
                        logger.info(f"{id} -- broadcast -- GAMEOVER")
                    else:
                        
                        if id == "0":
                            p0.cards = p0.cards[1:]
                            p0.state = "MISTAKE"
                        if id == "1":
                            p1.cards = p1.cards[1:]
                            p1.state = "MISTAKE"
                        if id == "2":
                            p2.cards = p2.cards[1:]
                            p2.state = "MISTAKE"

                        logger.info(f"{id} -- MISTAKE")
                        sendit = "MISTAKE " + str(card_played)
                        broadcast(clients, sendit.encode())
                        logger.info(f"{id} -- broadcast -- {sendit}")
            
            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAME" and msg == "MISTAKE":
                if id == "0":
                    p0.state = "MISTAKE"
                if id == "1":
                    p1.state = "MISTAKE"
                if id == "2":
                    p2.state = "MISTAKE"
                logger.info(f"{id} -- MISTAKE")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAME" and msg == "ASK_REFOCUS": 
                if id == "0":
                    p0.state = "REFOCUS"
                if id == "1":
                    p1.state = "REFOCUS"
                if id == "2":
                    p2.state = "REFOCUS"
                logger.info(f"{id} -- REFOCUS")
                broadcast(clients, "REFOCUS".encode())
                logger.info(f"{id} -- broadcast -- REFOCUS")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "REFOCUS" and msg == "REFOCUS":
                if id == "0":
                    p0.state = "REFOCUS"
                if id == "1":
                    p1.state = "REFOCUS"
                if id == "2":
                    p2.state = "REFOCUS"
                logger.info(f"{id} -- REFOCUS")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAMEOVER" and msg == "GAMEOVER":
                if id == "0":
                    p0.state = "GAMEOVER"
                if id == "1":
                    p1.state = "GAMEOVER"
                if id == "2":
                    p2.state = "GAMEOVER"
                logger.info(f"{id} -- GAMEOVER")


def main():
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 

    logger = setup_logger("main")
    logger.info(f'Connected to Player {id}') 

    topPile = 0
    gameState = "WELCOME"
    level = 1
    lives = 3
    clients = []
    p0 = Player("0")
    p1 = Player("1")
    p2 = Player("2")
    card_played = 0
    player_played = []

    host = '192.168.1.169'
    port = 50001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        logger.info(f'Server listening on {host}:{port}')

        threading.Thread(target=gameManager, args=(server_socket, )).start()
        logger.info(f'gameManager start')


        for i in range(3):
            conn, addr = server_socket.accept()
            first = conn.recv(1024)
            first = first.decode()
            player_id = ''.join(x for x in first if x.isdigit())
            threading.Thread(target=on_new_client, args=(conn, addr, player_id, )).start()
            logger.info(f'start {player_id}')
            #conn.close()
            
if __name__ == '__main__':
    main()



