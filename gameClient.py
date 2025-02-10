import multiprocessing
import time
import socket
import sys
import pygame 
import logging
import os
import threading

#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL) 
#file_path = os.path.join('/storage/emulated/0/', 'pydroid_logs.log')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

global cards, state, level, lastplay, mistake

# Function to be executed in the parallel process
def worker(s, id):
    global cards, state, level, lastplay, mistake
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        print(">"+msg)
        logging.debug('>'+msg)
       
        if "NEXTLEVEL" in msg:
            list_cards = eval(msg[9:])
            cards = list_cards[int(id)]
            level = len(list_cards[int(id)])
            state = "NEXTLEVEL"
        
        elif "GAMEOVER" in msg:
            state = "GAMEOVER"
            cards = []
            level = 0
            lastplay = 0
            mistake = 0

            #print(state)

        elif "GAME" in msg:
            state = "GAME"
        
        elif "WELCOME" in msg:
            state = "WELCOME"

        elif len(cards) > 0:
            if "MISTAKE" in msg:
                state = "MISTAKE"
                mistake = int(msg[7:])
                cards = [x for x in cards if x > mistake]
            
            if "REFOCUS" in msg:
                state = "REFOCUS"

def main():
    global cards, state, level, lastplay, mistake

    cards = []
    state = "WELCOME"
    level = 0
    lastplay = 0
    mistake = 0

    # initializing the constructor 
    pygame.init() 
    
    # screen resolution 
    res = (720,720) 
    screen = pygame.display.set_mode(res) 
    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35) 
    
    id = sys.argv[1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('127.0.0.1', 50001))
    msgid = "Player " + id
    s.send(msgid.encode())


    threading.Thread(target=worker, args=(s, id, )).start()

    width = screen.get_width() 
    height = screen.get_height()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                continue 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "WELCOME":
                    s.send("WELCOME".encode())
                    state = "WAITING_WELCOME"
                    
                elif state == "NEXTLEVEL":
                    s.send("READYTOPLAY".encode())
                    state = "WAITING_NEXTLEVEL"

                elif state  == "GAME" and len(cards) > 0:
                    if width/5 <= mouse[0] <= width/5+120 and height/5 <= mouse[1] <= height/5+100: 
                        s.send("ASK_REFOCUS".encode())
                        state = "ASK_REFOCUS" 
                    if width/2.5 <= mouse[0] <= width/2.5+120 and height/2.5 <= mouse[1] <= height/2.5+100:
                        tosend = "PLAY " +  str(cards[0])
                        s.send(tosend.encode())
                        lastplay = cards[0]
                        cards = cards[1:]
                
                elif state == "MISTAKE":
                    s.send("MISTAKE".encode())
                    state = "WAITING_MISTAKE"
                
                elif state == "REFOCUS":
                    s.send("REFOCUS".encode())
                    state = "WAITING_REFOCUS"

                elif state == "GAMEOVER":
                    s.send("GAMEOVER".encode())
                    state = "WAITING_GAMEOVER"


        mouse = pygame.mouse.get_pos() 

        #print(state)
        if state == "WELCOME":
            screen.fill((231,84,128))  
            text = font.render("LEVEL "+ str(level+1), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
                
            pygame.display.flip()
        if state == "WAITING_WELCOME":
            screen.fill((255,182,193)) 
            text = font.render("LEVEL "+ str(level+1), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
                
            pygame.display.flip()
        
        elif state == "NEXTLEVEL":
            screen.fill((15,170,240)) 
            text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            cards_text = font.render(str(cards), True, (0, 0, 0))
            text_width, text_height = cards_text.get_size()
            x = (width - text_width) // 2
            if x < 0:
                x = 0
            screen.blit(cards_text, (x,screen.get_rect().centery - 200))
            pygame.display.flip()
        
        elif state == "WAITING_NEXTLEVEL":
            screen.fill((151,214,242)) 
            text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            text_width, text_height = cards_text.get_size()
            x = (width - text_width) // 2
            if x < 0:
                x = 0
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, (x,screen.get_rect().centery - 200))
            pygame.display.flip()

        elif state  == "GAME" and len(cards) > 0:
            screen.fill((255,255,255)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            text_width, text_height = cards_text.get_size()
            x = (width - text_width) // 2
            if x < 0:
                x = 0
            screen.blit(cards_text, (x ,height/1.5))

            if width/5 <= mouse[0] <= width/5+120 and height/5 <= mouse[1] <= height/5+100: 
                pygame.draw.rect(screen,(178,223,138) ,[width/5,height/5,120,100]) 

            else: 
                pygame.draw.rect(screen,(51,160,44) ,[width/5,height/5,120,100])
            
            text = smallfont.render('refocus' , True , (0,0,0) )
            screen.blit(text , (width/5+10,height/5+30)) 

            if width/2.5 <= mouse[0] <= width/2.5+120 and height/2.5 <= mouse[1] <= height/2.5+100: 
                pygame.draw.rect(screen,(178,223,138) ,[width/2.5,height/2.5,120,100]) 

            else: 
                pygame.draw.rect(screen,(51,160,44) ,[width/2.5,height/2.5,120,100])

            text = smallfont.render('play' , True , (0,0,0) )
            screen.blit(text , (width/2.5+30,height/2.5+30)) 
            
            pygame.display.flip()

        elif state  == "GAME" and len(cards) == 0:
            screen.fill((200,200,200)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()
        
        elif state  == "MISTAKE":
            screen.fill((223,28,28)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()
        
        elif state  == "WAITING_MISTAKE":
            screen.fill((242,110,110)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        elif state  == "REFOCUS":
            screen.fill((51,160,44)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        elif state  == "WAITING_REFOCUS":
            screen.fill((178,223,138)) 
            cards_text = font.render(str(cards), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()


        if state == "GAMEOVER":
            screen.fill((255,140,0)) 
            text = font.render("GAME OVER", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()
        
        if state == "WAITING_GAMEOVER":
            screen.fill((255, 194, 75)) 
            text = font.render("GAME OVER", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

if __name__ == "__main__":
    main()