#!/usr/bin/python                                                                                                                                                                      

import socket               
import multiprocessing
import socket
import multiprocessing
import json
import time
import random

#GameState: NEXTLEVEL, REFOCUS, GAME, MISTAKE, USESTAR, DEALCARDS
#playerState: NEXTLEVEL, READYTOPLAY

class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []
        self.state = "NEXTLEVEL"

def broadcast(clients, message):          
        for client in clients : 
            client.send(message)

def getCards(level):
    cards = random.sample(range(1, 100), 3*level)
    lists_cards = [ cards[i:i+level] for i in range(0, len(cards), level) ]
    return sorted(lists_cards[0]), sorted(lists_cards[1]), sorted(lists_cards[2])
    
def gameManager(server_socket,shared_data, shared_data_lock):
    print("START")
    while True:
        with shared_data_lock:
            #print(shared_data)
            if shared_data["gameState"] == "NEXTLEVEL" and  shared_data["player0State"] == "NEXTLEVEL" and  shared_data["player1State"] == "NEXTLEVEL" and  shared_data["player2State"] == "NEXTLEVEL" and shared_data["player0Cards"] == [] and shared_data["player1Cards"] == [] and shared_data["player2Cards"] == []:
                cards_p0, cards_p1, cards_p2 = getCards(shared_data["level"])
                shared_data["player0Cards"] = cards_p0
                shared_data["player1Cards"] = cards_p1
                shared_data["player2Cards"] = cards_p2
                
                #broadcast(shared_data["clients"], "NEXTLEVEL".encode())
                #print("nextlevel")

            if shared_data["gameState"] == "NEXTLEVEL" and  shared_data["player0State"] == "REFOCUS" and  shared_data["player1State"] == "REFOCUS" and  shared_data["player2State"] == "REFOCUS":
                shared_data["gameState"] = "REFOCUS"
                
                broadcast(shared_data["clients"], "REFOCUS".encode())
                print("refocus")

            if shared_data["gameState"] == "REFOCUS" and  shared_data["player0State"] == "GAME" and  shared_data["player1State"] == "GAME" and  shared_data["player2State"] == "GAME":
                shared_data["gameState"] = "GAME"
                broadcast(shared_data["clients"], "GAME".encode())
                print("game")

            if shared_data["gameState"] == "GAME" and shared_data["topPile"] != 0:
                print(shared_data["topPile"])

            if shared_data["gameState"] == "GAME" and  shared_data["player0State"] == "NEXTLEVEL" and  shared_data["player1State"] == "NEXTLEVEL" and  shared_data["player2State"] == "NEXTLEVEL" and shared_data["topPile"] != 0 and shared_data["player0Cards"] == [] and shared_data["player1Cards"] == [] and shared_data["player2Cards"] == []:
                shared_data["level"] += 1
                shared_data["gameState"] = "NEXTLEVEL"
                shared_data["topPile"] = 0
                broadcast(shared_data["clients"], "NEXTLEVEL".encode())
   
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
            with shared_data_lock: 
                if shared_data["player"+id+"State"] == "NEXTLEVEL" and shared_data["gameState"] == "NEXTLEVEL"  and msg == "READYTOPLAY" and shared_data["player"+id+"Cards"] != []: 
                    conn.send(str(shared_data["player"+id+"Cards"]).encode())
                    shared_data["player"+id+"State"] = "REFOCUS"

                if shared_data["player"+id+"State"] == "REFOCUS" and shared_data["gameState"] == "REFOCUS"  and msg == "REFOCUS":
                    shared_data["player"+id+"State"] = "GAME"

                if shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and msg.isdigit():
                    shared_data["topPile"] = int(msg)
                    shared_data["player"+id+"Cards"] = shared_data["player"+id+"Cards"][1:]

                if shared_data["player"+id+"State"] == "GAME" and shared_data["gameState"] == "GAME" and shared_data["player"+id+"Cards"] == []:
                    shared_data["player"+id+"State"] = "NEXTLEVEL"

                              
def main():
    HOST = '127.0.0.1'
    PORT = 50001
    with multiprocessing.Manager() as manager:
        shared_data = manager.dict({"topPile": 0,"gameState":"NEXTLEVEL", "level":1 ,"player0State": "NEXTLEVEL", "player0Cards": [],"player1State": "NEXTLEVEL", "player1Cards": [],"player2State": "NEXTLEVEL", "player2Cards": [], "clients": []})
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



