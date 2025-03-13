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
import os

mutex = threading.Lock()

#GameState: NEXTLEVEL, REFOCUS, GAME, MISTAKE, USESTAR, DEALCARDS
#playerState: NEXTLEVEL, READYTOPLAY

def setup_logger(process_name):

    directory = "migas"

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

class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.state = "WELCOME"
        self.lost = []
    
    def print_player(self):
        return str(self.id) + " " + str(self.state) + " " + str(self.cards)  + " " + str(self.lost) 

def broadcast(clients, message): 
        print(message)         
        for client in clients : 
            client.send(message)

def getCards(Level):
    cards = []

    if Level == 1:
        cards.append(random.randint(1, 20))
        cards.append(random.randint(50, 60))
        cards.append(random.randint(90, 99))
        random.shuffle(cards)

    elif Level == 2:
        while len(cards) < 5:
            next_card = random.randint(50, 99)
            if next_card not in cards:
                cards.append(next_card)

        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 99:
                cards.append(c)
                b = False

    elif Level == 3:
        while len(cards) < 7:
            next_card = random.randint(1, 99)
            if next_card not in cards:
                cards.append(next_card)
        b = True
        while b:
            c = cards[random.randint(2, 6)] + 3
            if c not in cards and c < 99:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(2, 7)] + 1
            if c not in cards  and c < 99:
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
                next_card = random.randint(75, 99)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(4, 6)] + 2
            if c not in cards and c < 99:
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
                next_card = random.randint(70, 99)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 3)] + 2
            if c not in cards and c < 99:
                cards.insert(4, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 9)] + 5
            if c not in cards and c < 99:
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
                next_card = random.randint(70, 99)
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
                next_card = random.randint(40, 99)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(0, 5)] + 2
            if c not in cards and c < 99:
                cards.insert(6, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(7, 13)] + 1
            if c not in cards and c < 99:
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
                next_card = random.randint(50, 99)
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
                next_card = random.randint(50, 99)
                if next_card not in cards:
                    cards.append(next_card)
                    g += 1
        b = True
        while b:
            c = cards[random.randint(9, 16)] + 3
            if c not in cards and c < 99:
                cards.insert(17, c)
                b = False
        b = True
        while b:
            c = cards[random.randint(0, 8)] + 1
            if c not in cards and c < 99:
                cards.append(c)
                b = False

    elif Level == 10:
        while len(cards) < 30:
            next_card = random.randint(1, 99)
            if next_card not in cards:
                cards.append(next_card)

    # Distribute cards to each player
    hands = []
    for i in range(3):
        hand = cards[i*Level : (i + 1)*Level]
        hands.append(sorted(hand))

    return hands

global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played, card_pile 

def gameManager(server_socket):
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played, card_pile 
    logger = setup_logger("gameManager")

    ultima = False
    last = False
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 50
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.Font("TT Rounds Neue Trial Black.ttf",200)
    fontinfo = pygame.font.Font("TT Rounds Neue Trial Regular.ttf",50)
    fonttoppile = pygame.font.Font("TT Rounds Neue Trial Black.ttf",70)
    fontinfocards = pygame.font.Font("TT Rounds Neue Trial Black.ttf",80)

    image = pygame.image.load("arrow.png").convert_alpha()
    image = pygame.transform.scale(image, (150, 150))

    image_hand = pygame.image.load("hand.png").convert_alpha()
    image_hand = pygame.transform.scale(image_hand, (150, 150))
   

    pygame.mixer.init() 
    sound = pygame.mixer.Sound("card-sound.mp3")
    
    win_time = None
    ultima_time = None
    mistake_time = None
   
    run = True

    while run:
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gameState == "GAMEOVER" and p0.state == "GAMEOVER" and  p1.state == "GAMEOVER" and  p2.state == "GAMEOVER":
                    with mutex:
                        logger.info("GAMEOVER")
                        topPile = 0
                        gameState = "WELCOME"
                        level = 1 
                        lives = 5
                        p0.state = "WELCOME"
                        p0.cards =  []
                        p1.state = "WELCOME"
                        p1.cards = []
                        p2.state = "WELCOME"
                        p2.cards = []

                    logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")

                    tosend = "WELCOME"
                    broadcast(clients, tosend.encode())
                    logger.info("broadcast: WELCOME")

        #p0.print_player()
        #p1.print_player()
        #p2.print_player()

        print(str(card_pile) +  " " + gameState+ " " + p0.print_player() + " " + p1.print_player() + " " + p2.print_player())

        if len(p0.cards) == 0 and len(p1.cards) == 0 and len(p2.cards) == 1:
            print("last")
            if not last:
                logger.info("only player2 as cards")
                broadcast(clients, "LAST".encode())
                logger.info("broadcast: LAST")
                last = True
        
        if gameState == "WELCOME" and  p0.state == "NEXTLEVEL" and  p1.state == "NEXTLEVEL" and  p2.state == "NEXTLEVEL":
            with mutex:
                gameState = "NEXTLEVEL"
                last = False
                cards_p0, cards_p1, cards_p2 = getCards(level)
                p0.cards = cards_p0
                p1.cards = cards_p1
                p2.cards = cards_p2
                cards = [cards_p0, cards_p1, cards_p2]
            
            logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")
            tosend = "NEXTLEVEL " + str(cards)
            broadcast(clients, tosend.encode())
            logger.info(f"broadcast: {tosend}")

        elif gameState == "NEXTLEVEL" and  p0.state == "GAME" and  p1.state == "GAME" and  p2.state == "GAME":
            gameState = "GAME"
            logger.info("state: GAME")
            broadcast(clients, "GAME".encode())
            logger.info("broadcast: GAME")

        elif gameState == "GAME" and card_pile != []:
            
            with mutex:
                card_played = card_pile[0][0]
                print(card_pile)
                print(str(p0.cards) + " " + str(p1.cards) + " " + str(p2.cards))
                topPile = card_played
                id = card_pile[0][1]
                player_played = [card_pile[0][1] , card_pile[0][2]] 
                card_pile.pop(0)
            logger.info(f"PLAY -- palyer: {id} -- card: {card_played}")
            #playsound("card-sound.mp3")
            sound.play()


            if (len(p0.cards) == 0 or card_played <= p0.cards[0]) and (len(p1.cards) == 0 or card_played <= p1.cards[0]) and (len(p2.cards) == 0 or card_played <= p2.cards[0]):
                
                if id == "0":
                    with mutex:
                        p0.cards = p0.cards[1:]
                if id == "1":
                    with mutex:
                        p1.cards = p1.cards[1:]
                if id == "2":
                    with mutex:
                        p2.cards = p2.cards[1:]

                logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")
                sendit = f"CARD {id},{str(card_played)}"
                broadcast(clients, sendit.encode())
                logger.info(f"broadcast: {sendit}")
                
            else:
                with mutex:
                    lives -= 1
                logger.info(f'lives: {lives}')
                
                if id == "0":
                    with mutex:
                        p0.lost = [x for x in p0.cards if x <= topPile]
                        p0.cards = [x for x in p0.cards if x > topPile]
                        p1.lost = [x for x in p1.cards if x <= topPile]
                        p1.cards = [x for x in p1.cards if x > topPile]
                        p2.lost = [x for x in p2.cards if x <= topPile]
                        p2.cards = [x for x in p2.cards if x > topPile]
                        p0.state = "MISTAKE"
                        gameState = "MISTAKE"
                        mistake_time = time.time()
                if id == "1":
                    with mutex:
                        p0.lost = [x for x in p0.cards if x <= topPile]
                        p0.cards = [x for x in p0.cards if x > topPile]
                        p1.lost = [x for x in p1.cards if x <= topPile]
                        p1.cards = [x for x in p1.cards if x > topPile]
                        p2.lost = [x for x in p2.cards if x <= topPile]
                        p2.cards = [x for x in p2.cards if x > topPile]
                        p1.state = "MISTAKE"
                        gameState = "MISTAKE"
                        mistake_time = time.time()
                if id == "2":
                    with mutex:
                        p0.lost = [x for x in p0.cards if x <= topPile]
                        p0.cards = [x for x in p0.cards if x > topPile]
                        p1.lost = [x for x in p1.cards if x <= topPile]
                        p1.cards = [x for x in p1.cards if x > topPile]
                        p2.lost = [x for x in p2.cards if x <= topPile]
                        p2.cards = [x for x in p2.cards if x > topPile]
                        p2.state = "MISTAKE"
                        gameState = "MISTAKE"
                        mistake_time = time.time()

                logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")
                sendit = "MISTAKE " + str(card_played)
                broadcast(clients, sendit.encode())
                logger.info(f"broadcast: {sendit}")
            

        elif gameState == "GAME" and  len(p0.cards) == 0 and len(p1.cards) == 0 and len(p2.cards) == 0 and ultima == False:
            ultima_time = time.time()
            ultima = True
            logger.info(f"Last card was played")

        elif gameState == "GAME" and  len(p0.cards) == 0 and len(p1.cards) == 0 and len(p2.cards) == 0 and time.time() - ultima_time >= 2:
            level += 1
            logger.info(f'level: {level}')

            time.sleep(2)

            if level == 10:
                with mutex:
                    gameState = "WIN"
                win_time = time.time()
                logger.info("state: WIN")
                
            else:
                with mutex:
                    gameState = "WELCOME"
                    topPile = 0
                    p0.state = "WELCOME"
                    p1.state = "WELCOME"
                    p2.state = "WELCOME"
                    logger.info("WELCOME")
                    cards = [cards_p0, cards_p1, cards_p2]
                logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")
                tosend = "WELCOME " + str(cards)
                broadcast(clients, tosend.encode())
                logger.info(f"broadcast -- {tosend}")
            
            ultima = False

        elif gameState == "MISTAKE" and  (len(p0.cards) == 0 or p0.state == "MISTAKE") and  (len(p1.cards) == 0 or p1.state == "MISTAKE") and  (len(p2.cards) == 0 or p2.state == "MISTAKE"):
            if time.time() - mistake_time >= 3:
                with mutex:
                    #p0.cards = [x for x in p0.cards if x >= topPile]
                    #p1.cards = [x for x in p1.cards if x >= topPile]
                    #p2.cards = [x for x in p2.cards if x >= topPile]
                    gameState = "GAME"
                    p0.state = "GAME"
                    p1.state = "GAME"
                    p2.state = "GAME"
                    p0.lost = []
                    p1.lost = []
                    p2.lost = []
                print("mistake")
                if lives == 0:
                    with mutex:
                        gameState = "GAMEOVER"
                    logger.info(f"state: {gameState} -- p0.state: {p0.state} -- p0.cards: {p0.cards}  -- p1.state: {p1.state} -- p1.cards: {p1.cards}  -- p2.state: {p2.state} -- p2.cards: {p2.cards}")
                    broadcast(clients, "GAMEOVER".encode())
                    logger.info(f"broadcast: GAMEOVER")
                else:
                    logger.info("state: GAME")
                    broadcast(clients, "GAME".encode())
                    logger.info("broadcast: GAME")

        elif gameState == "GAME" and (p0.state == "REFOCUS" or p1.state == "REFOCUS" or p2.state == "REFOCUS"):
            with mutex:
                gameState = "REFOCUS"
                p0.state = "GAME"
                p1.state = "GAME"
                p2.state = "GAME"
            logger.info("state: REFOCUS")

        elif gameState == "REFOCUS" and  (len(p0.cards) == 0 or p0.state == "REFOCUS") and  (len(p1.cards) == 0 or p1.state == "REFOCUS") and  (len(p2.cards) == 0 or p2.state == "REFOCUS"):
            with mutex:
                gameState = "GAME"
                p0.state = "GAME"
                p1.state = "GAME"
                p2.state = "GAME"
            logger.info(f"state: GAME")
            broadcast(clients, "GAME".encode())
            logger.info("broadcast: GAME")

        elif gameState == "WIN":

            if time.time() - win_time >= 2:
                with mutex:
                    gameState = "GAMEOVER"
                logger.info("GAMEOVER")
                broadcast(clients, "GAMEOVER".encode())
                logger.info("broadcast: GAMEOVER")

        if gameState == "WELCOME":

            screen.fill((231,84,128))

            text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0x = 40
            pl0y = height-100
            pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
            screen.blit(pl0,(pl0x,pl0y))
            pl01 = fontinfocards.render(str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
            pl02 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
            
            pl1x = width-350
            pl1y = height-100
            pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
            screen.blit(pl1,(pl1x,pl1y))
            pl11 = fontinfocards.render(str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
            pl12 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))

            pl2x = width/2-150
            pl2y = 40
            pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
            screen.blit(pl2,(pl2x,pl2y))
            pl21 = fontinfocards.render(str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
            pl22 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))
            
            pygame.display.flip()

        
        elif gameState == "NEXTLEVEL":
            
            screen.fill((15,170,240))

            text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0x = 40
            pl0y = height-100
            pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
            screen.blit(pl0,(pl0x,pl0y))
            pl01 = fontinfocards.render(str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
            pl02 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
            
            pl1x = width-350
            pl1y = height-100
            pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
            screen.blit(pl1,(pl1x,pl1y))
            pl11 = fontinfocards.render(str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
            pl12 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))

            pl2x = width/2-150
            pl2y = 40
            pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
            screen.blit(pl2,(pl2x,pl2y))
            pl21 = fontinfocards.render(str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
            pl22 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))

            if p0.state == "GAME":
                angle = -45
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width/4, height*(3/4)))
                screen.blit(rotated_image, rect.topleft)

            if p1.state == "GAME":
                angle = 45
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width*(3/4), height*(3/4)))
                screen.blit(rotated_image, rect.topleft)
                
            if p2.state == "GAME":
                angle = -180
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width/2, height/4))
                screen.blit(rotated_image, rect.topleft)
            
            pygame.display.flip()

        
        elif gameState == "GAME":
            
            screen.fill((255, 255, 255))
            
            pygame.draw.rect(screen,(255, 193, 7) , (width/2-175,height/2-150,350,300))
            text = font.render(str(topPile), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lev = fontinfo.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(lev, (10,80))
            liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0x = 40
            pl0y = height-100
            pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
            screen.blit(pl0,(pl0x,pl0y))
            pl01 = fontinfocards.render(str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
            pl02 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
            
            pl1x = width-350
            pl1y = height-100
            pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
            screen.blit(pl1,(pl1x,pl1y))
            pl11 = fontinfocards.render(str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
            pl12 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))

            pl2x = width/2-150
            pl2y = 40
            pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
            screen.blit(pl2,(pl2x,pl2y))
            pl21 = fontinfocards.render(str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
            pl22 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))
            

            if len(player_played) > 0 and time.time() - player_played[1] < 2:
            
                if player_played[0] == "0":
                    #print(player_played)
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

        elif gameState == "MISTAKE":
            
            screen.fill((223, 28, 28))
            
            
            pygame.draw.rect(screen,(255, 193, 7) , (width/2-175,height/2-150,350,300))
            text = font.render(str(topPile), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lev = fontinfo.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(lev, (10,80))
            liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0x = 40
            pl0y = height-100
            pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
            screen.blit(pl0,(pl0x,pl0y))
            pl01 = fontinfocards.render(str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
            pl02 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
            pl0lost = fontinfo.render(str(p0.lost), True, (0, 0, 0)) 
            screen.blit(pl0lost,(pl0x,pl0y-100))
            
            pl1x = width-350
            pl1y = height-100
            pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
            screen.blit(pl1,(pl1x,pl1y))
            pl11 = fontinfocards.render(str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
            pl12 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))
            pl1lost = fontinfo.render(str(p1.lost), True, (0, 0, 0)) 
            screen.blit(pl1lost,(pl1x,pl0y-100))

            pl2x = width/2-150
            pl2y = 40
            pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
            screen.blit(pl2,(pl2x,pl2y))
            pl21 = fontinfocards.render(str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
            pl22 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))
            pl2lost = fontinfo.render(str(p2.lost), True, (0, 0, 0)) 
            screen.blit(pl2lost,(pl2x,pl2y+100))

            if len(player_played) > 0 and time.time() - player_played[1] < 2:
            
                if player_played[0] == "0":
                    #print(player_played)
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
            pygame.draw.rect(screen,(255, 193, 7) , (width/2-175,height/2-150,350,300))
            text = font.render(str(topPile), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lev = fontinfo.render("LEVEL: "+ str(level), True, (0, 0, 0))
            screen.blit(lev, (10,80))
            liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
            screen.blit(liv, (10,10))
            pl0x = 40
            pl0y = height-100
            pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
            screen.blit(pl0,(pl0x,pl0y))
            pl01 = fontinfocards.render(str(len(p0.cards)), True, (0, 0, 0))
            screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
            pl02 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
            
            pl1x = width-350
            pl1y = height-100
            pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
            screen.blit(pl1,(pl1x,pl1y))
            pl11 = fontinfocards.render(str(len(p1.cards)), True, (0, 0, 0))
            screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
            pl12 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))

            pl2x = width/2-150
            pl2y = 40
            pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
            screen.blit(pl2,(pl2x,pl2y))
            pl21 = fontinfocards.render(str(len(p2.cards)), True, (0, 0, 0))
            screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
            pl22 = fontinfo.render(" cards", True, (0, 0, 0))
            screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))

            if p0.state == "REFOCUS":
                angle = -45
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width/4, height*(3/4)))
                screen.blit(rotated_image, rect.topleft)

            if p1.state == "REFOCUS":
                angle = 45
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width*(3/4), height*(3/4)))
                screen.blit(rotated_image, rect.topleft)
                
            if p2.state == "REFOCUS":
                angle = -180
                rotated_image = pygame.transform.rotate(image_hand, angle)
                rect = rotated_image.get_rect(center=(width/2, height/4))
                screen.blit(rotated_image, rect.topleft)
            
            pygame.display.flip()
            
        elif gameState == "WIN":
            time.sleep(1)
            screen.fill((255,140,0)) 
            text = font.render("VICTORY", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        elif gameState == "GAMEOVER":
            time.sleep(1)
            screen.fill((255,140,0)) 
            text = font.render("PLAY AGAIN?", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

def on_new_client(conn, addr, id):
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played, card_pile

    logger = setup_logger(id)
    logger.info(f'Connected to Player {id}')
    
    clients.append(conn)

    with conn:
        while True:
            msg = conn.recv(1024)
            msg = msg.decode()
            logger.info(f"{id} -- message: {msg}")
            print(str(id) + " " + msg)
            
            if ((id == "0" and p0.state == "WELCOME") or (id == "1" and p1.state == "WELCOME")  or (id == "2" and p2.state == "WELCOME")) and gameState == "WELCOME" and msg == "WELCOME":   
                if id == "0":
                    with mutex:
                        p0.state = "NEXTLEVEL"
                if id == "1":
                    with mutex:
                        p1.state = "NEXTLEVEL"
                if id == "2":
                    with mutex:
                        p2.state = "NEXTLEVEL"
                logger.info(f"{id} -- state: NEXTLEVEL")

            elif ((id == "0" and p0.state == "NEXTLEVEL") or (id == "1" and p1.state == "NEXTLEVEL")  or (id == "2" and p2.state == "NEXTLEVEL")) and gameState == "NEXTLEVEL" and msg == "READYTOPLAY":   
                if id == "0":
                    with mutex:
                        p0.state = "GAME"
                if id == "1":
                    with mutex:
                        p1.state = "GAME"
                if id == "2":
                    with mutex:
                        p2.state = "GAME"
                logger.info(f"{id} -- state: GAME")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAME" and "PLAY" in msg:   
                with mutex:
                    card_pile.append([int(msg[5:]), id , time.time()])
                    #card_played = int(msg[5:])
                    #topPile = card_played
                    #player_played = [id , time.time()] 
                logger.info(f"{id} -- PLAY: {int(msg[5:])}")
                #playsound("card-sound.mp3")
            
            elif gameState == "MISTAKE" and msg == "MISTAKE":
                if id == "0":
                    with mutex:
                        p0.state = "MISTAKE"
                if id == "1":
                    with mutex:
                        p1.state = "MISTAKE"
                if id == "2":
                    with mutex:
                        p2.state = "MISTAKE"
                logger.info(f"{id} -- state: MISTAKE")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAME" and msg == "ASK_REFOCUS": 
                if id == "0":
                    with mutex:
                        p0.state = "REFOCUS"
                if id == "1":
                    with mutex:
                        p1.state = "REFOCUS"
                if id == "2":
                    with mutex:
                        p2.state = "REFOCUS"
                logger.info(f"{id} -- state: REFOCUS")
                broadcast(clients, "REFOCUS".encode())
                logger.info(f"{id} -- broadcast: REFOCUS")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "REFOCUS" and msg == "REFOCUS":
                if id == "0":
                    with mutex:
                        p0.state = "REFOCUS"
                if id == "1":
                    with mutex:
                        p1.state = "REFOCUS"
                if id == "2":
                    with mutex:
                        p2.state = "REFOCUS"
                logger.info(f"{id} -- state: REFOCUS")

            elif ((id == "0" and p0.state == "GAME") or (id == "1" and p1.state == "GAME")  or (id == "2" and p2.state == "GAME")) and gameState == "GAMEOVER" and msg == "GAMEOVER":
                if id == "0":
                    with mutex:
                        p0.state = "GAMEOVER"
                if id == "1":
                    with mutex:
                        p1.state = "GAMEOVER"
                if id == "2":
                    with mutex:
                        p2.state = "GAMEOVER"
                logger.info(f"{id} -- state: GAMEOVER")

def main():
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played, card_pile

    logger = setup_logger("main")
    logger.info(f'Connected to Player {id}') 
    
    with mutex:
        topPile = 0
        gameState = "WELCOME"
        level = 1
        lives = 5
        clients = []
        p0 = Player("0")
        p1 = Player("1")
        p2 = Player("2")
        card_played = 0
        player_played = []
        card_pile = []

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



