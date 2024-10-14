#!/usr/bin/python                                                                                                                                                                      

import socket
import multiprocessing
import random
import pygame

#GameState: NEXTLEVEL, REFOCUS, GAME, MISTAKE, USESTAR, DEALCARDS
#playerState: NEXTLEVEL, READYTOPLAY

class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.state = "NEXTLEVEL"

def broadcast(clients, message): 
        print(message)         
        for client in clients : 
            client.send(message)

def getCards(level):
    cards = random.sample(range(1, 100), 3*level)
    lists_cards = [ cards[i:i+level] for i in range(0, len(cards), level) ]
    return sorted(lists_cards[0]), sorted(lists_cards[1]), sorted(lists_cards[2])
    
def gameManager(server_socket,shared_data, shared_data_lock):
    print("START")
    pygame.init() 
    
    res = (720,720) 
    screen = pygame.display.set_mode(res) 
    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35)

    run = True
    while True:
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shared_data["gameState"] == "GAMEOVER" and  shared_data["player0State"] == "GAMEOVER" and  shared_data["player1State"] == "GAMEOVER" and  shared_data["player2State"] == "GAMEOVER":
                    with shared_data_lock:
                        shared_data["topPile"] = 0
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
                        print("hello")

        with shared_data_lock:
            if len(shared_data["player0Cards"]) == 0 and len(shared_data["player1Cards"]) == 0 and len(shared_data["player2Cards"]) == 1:
                #print("last")
                broadcast(shared_data["clients"], "LAST".encode())
            

            if shared_data["gameState"] == "WELCOME" and  shared_data["player0State"] == "NEXTLEVEL" and  shared_data["player1State"] == "NEXTLEVEL" and  shared_data["player2State"] == "NEXTLEVEL":
                shared_data["gameState"] = "NEXTLEVEL"
                cards_p0, cards_p1, cards_p2 = getCards(shared_data["level"])
                shared_data["player0Cards"] = cards_p0
                shared_data["player1Cards"] = cards_p1
                shared_data["player2Cards"] = cards_p2
                cards = [cards_p0, cards_p1, cards_p2]
                tosend = "NEXTLEVEL " + str(cards)
                #print(cards)
                broadcast(shared_data["clients"], tosend.encode())

            if shared_data["gameState"] == "NEXTLEVEL" and  shared_data["player0State"] == "GAME" and  shared_data["player1State"] == "GAME" and  shared_data["player2State"] == "GAME":
                shared_data["gameState"] = "GAME"
                broadcast(shared_data["clients"], "GAME".encode())

            if shared_data["gameState"] == "GAME" and  (len(shared_data["player0Cards"]) == 0 or shared_data["player0State"] == "MISTAKE") and  (len(shared_data["player1Cards"]) == 0 or shared_data["player1State"] == "MISTAKE") and  (len(shared_data["player2Cards"]) == 0 or shared_data["player2State"] == "MISTAKE"):
                shared_data["player0Cards"] = [x for x in shared_data["player0Cards"] if x >= shared_data["topPile"]]
                shared_data["player1Cards"] = [x for x in shared_data["player1Cards"] if x >= shared_data["topPile"]]
                shared_data["player2Cards"] = [x for x in shared_data["player2Cards"] if x >= shared_data["topPile"]]
                shared_data["gameState"] = "GAME"
                shared_data["player0State"] = "GAME"
                shared_data["player1State"] = "GAME"
                shared_data["player2State"] = "GAME"
                broadcast(shared_data["clients"], "GAME".encode())

            if shared_data["gameState"] == "GAME" and  len(shared_data["player0Cards"]) == 0 and len(shared_data["player1Cards"]) == 0 and len(shared_data["player2Cards"]) == 0:
                shared_data["level"] += 1

                if shared_data["level"] == 11:
                    shared_data["gameState"] == "GAMEOVER"
                    shared_data["player0State"] = "GAMEOVER"
                    shared_data["player1State"] = "GAMEOVER"
                    shared_data["player2State"] = "GAMEOVER"
                    broadcast(shared_data["clients"], "GAMEOVER".encode())
                else:
                    shared_data["gameState"] = "WELCOME"
                    shared_data["topPile"] = 0
                    shared_data["player0State"] = "WELCOME"
                    shared_data["player1State"] = "WELCOME"
                    shared_data["player2State"] = "WELCOME"
                    cards = [cards_p0, cards_p1, cards_p2]
                    tosend = "WELCOME " + str(cards)
                    #print(cards)
                    broadcast(shared_data["clients"], tosend.encode())

            if shared_data["gameState"] == "REFOCUS" and  (len(shared_data["player0Cards"]) == 0 or shared_data["player0State"] == "REFOCUS") and  (len(shared_data["player1Cards"]) == 0 or shared_data["player1State"] == "REFOCUS") and  (len(shared_data["player2Cards"]) == 0 or shared_data["player2State"] == "REFOCUS"):
                shared_data["gameState"] = "GAME"
                shared_data["player0State"] = "GAME"
                shared_data["player1State"] = "GAME"
                shared_data["player2State"] = "GAME"
                broadcast(shared_data["clients"], "GAME".encode())

            #if shared_data["gameState"] == "GAMEOVER" and  shared_data["player0State"] == "GAMEOVER" and  shared_data["player1State"] == "GAMEOVER" and  shared_data["player2State"] == "GAMEOVER":
                #print("gameOver aqui em cima")
                #input("Play again?")
                #shared_data = {"topPile": 0,"gameState":"WELCOME", "level":1 ,"lives": 3, "player0State": "WELCOME", "player0Cards": [],"player1State": "WELCOME", "player1Cards": [],"player2State": "WELCOME", "player2Cards": [], "clients": []}
        
        #print(shared_data["gameState"])

        if shared_data["gameState"] == "WELCOME":
            #print("aiaia")
            screen.fill((231,84,128))

            text = font.render("LEVEL "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            pygame.display.flip()
        
        elif shared_data["gameState"] == "NEXTLEVEL":
            
            screen.fill((15,170,240))

            text = font.render("LEVEL "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            pygame.display.flip()
        
        elif shared_data["gameState"] == "GAME":
        
            if shared_data["player0State"] == "MISTAKE" or shared_data["player1State"] == "MISTAKE" or shared_data["player2State"] == "MISTAKE":
                screen.fill((223,28,28)) 
            else:
                screen.fill((255,255,255)) 
            text = font.render(str(shared_data["topPile"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            level = font.render("LEVEL: "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(level, (10,80))
            pygame.display.flip()
        
        elif shared_data["gameState"] == "REFOCUS":
            screen.fill((51,160,44)) 
            text = font.render(str(shared_data["topPile"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            lives = font.render("LIVES: "+ str(shared_data["lives"]), True, (0, 0, 0))
            screen.blit(lives, (10,10))
            level = font.render("LEVEL: "+ str(shared_data["level"]), True, (0, 0, 0))
            screen.blit(level, (10,80))
            pygame.display.flip()

        if shared_data["gameState"] == "GAMEOVER":
            screen.fill((255,140,0)) 
            text = font.render("PLAY AGAIN?", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()


def on_new_client(conn, addr, id, shared_data, shared_data_lock):
    print(f'Connected to Player {id}')
    with shared_data_lock: 
        clients = shared_data["clients"]
        clients.append(conn)
        shared_data["clients"] = clients
        
    with conn:
        while True:
            msg = conn.recv(1024)
            msg = msg.decode()
            #print(msg)
            with shared_data_lock: 
                
                if shared_data["player"+id+"State"] == "WELCOME" and shared_data["gameState"] == "WELCOME" and msg == "WELCOME": 
                   shared_data["player"+id+"State"] = "NEXTLEVEL"

                elif shared_data["player"+id+"State"] == "NEXTLEVEL" and shared_data["gameState"] == "NEXTLEVEL" and msg == "READYTOPLAY": 
                   shared_data["player"+id+"State"] = "GAME"

                elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and "PLAY" in msg:  
                    card_played = int(msg[5:])
                    if (len(shared_data["player0Cards"]) == 0 or card_played <= shared_data["player0Cards"][0]) and (len(shared_data["player1Cards"]) == 0 or card_played <= shared_data["player1Cards"][0]) and (len(shared_data["player2Cards"]) == 0 or card_played <= shared_data["player2Cards"][0]):
                        shared_data["topPile"] = card_played
                        shared_data["player"+id+"Cards"] = shared_data["player"+id+"Cards"][1:]
                        sendit = "CARD " + str(card_played) 
                        broadcast(shared_data["clients"], sendit.encode())
                    else:
                        shared_data["lives"] -= 1
                        
                        if shared_data["lives"] == 0:
                            #game over
                            #print("gameover")
                            shared_data["gameState"] = "GAMEOVER"
                            shared_data["player0State"] = "GAMEOVER"
                            shared_data["player1State"] = "GAMEOVER"
                            shared_data["player2State"] = "GAMEOVER"
                            broadcast(shared_data["clients"], "GAMEOVER".encode())
                        else:
                            shared_data["topPile"] = card_played
                            shared_data["player"+id+"Cards"] = shared_data["player"+id+"Cards"][1:]
                            shared_data["player"+id+"State"] = "MISTAKE"
                            sendit = "MISTAKE " + str(card_played)
                            broadcast(shared_data["clients"], sendit.encode())
                
                elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and msg == "MISTAKE": 
                    shared_data["player"+id+"State"] = "MISTAKE"
                
                elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and msg == "ASK_REFOCUS": 
                    shared_data["gameState"] = "REFOCUS"
                    broadcast(shared_data["clients"], "REFOCUS".encode())

                elif shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "REFOCUS" and msg == "REFOCUS": 
                    shared_data["player"+id+"State"] = "REFOCUS"

            #print(shared_data["player0Cards"])
            #print(shared_data["player1Cards"])
            #print(shared_data["player2Cards"])
                        
def main():
    HOST = '192.168.1.170'
    PORT = 50001


    with multiprocessing.Manager() as manager:
        shared_data = manager.dict({"topPile": 0,"gameState":"WELCOME", "level":1 ,"lives": 3, "player0State": "WELCOME", "player0Cards": [],"player1State": "WELCOME", "player1Cards": [],"player2State": "WELCOME", "player2Cards": [], "clients": []})
        shared_data_lock = manager.Lock()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f'Server listening on {HOST}:{PORT}')

            process = multiprocessing.Process(target=gameManager, args=(server_socket,shared_data, shared_data_lock))
            process.start()

   
            while True:
                conn, addr = server_socket.accept()
                first = conn.recv(1024)
                first = first.decode()
                id = ''.join(x for x in first if x.isdigit())
                process = multiprocessing.Process(target=on_new_client, args=(conn, addr, id, shared_data, shared_data_lock))
                process.start()
                conn.close()
               

if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    main()



