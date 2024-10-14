import multiprocessing
import time
import socket
import sys
import pygame 


# Function to be executed in the parallel process
def worker(shared_dict, shared_data_lock, s, id):
    while True:
        msg = s.recv(1024)
        msg = msg.decode()
        #print(">"+msg)
        with shared_data_lock:
            if "NEXTLEVEL" in msg:
                list_cards = eval(msg[9:])
                shared_dict["cards"] = list_cards[id]
                shared_dict["level"] = len(list_cards[id])
                shared_dict['state'] = "NEXTLEVEL"
            
            if "GAME" in msg:
                shared_dict['state'] = "GAME"
            
            if "WELCOME" in msg:
                shared_dict['state'] = "WELCOME"

            if len(shared_dict["cards"]) > 0:
                if "MISTAKE" in msg:
                    shared_dict['state'] = "MISTAKE"
                    shared_dict['mistake'] = int(msg[7:])
                    shared_dict["cards"] = [x for x in shared_dict["cards"] if x > shared_dict["mistake"]]
                
                if "REFOCUS" in msg:
                    shared_dict['state'] = "REFOCUS"

            if "GAMEOVER" in msg:
                shared_dict['state'] = "GAMEOVER"
                shared_dict = {"cards": [], "state": "WELCOME", "level" : 0, "lastplay": 0, "mistake": 0}


def main():
    # initializing the constructor 
    pygame.init() 
    
    # screen resolution 
    res = (720,720) 
    screen = pygame.display.set_mode(res) 
    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35) 

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
    s.connect(('192.168.1.170', 50001))
    msgid = "Player 1"
    s.send(msgid.encode())

    manager = multiprocessing.Manager()
    shared_dict = manager.dict({"cards": [], "state": "WELCOME", "level" : 0, "lastplay": 0, "mistake": 0})
    shared_data_lock = manager.Lock()

    worker_process = multiprocessing.Process(target=worker, args=(shared_dict, shared_data_lock, s, 1, ))
    worker_process.start()

    width = screen.get_width() 
    height = screen.get_height()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shared_dict["state"] == "WELCOME":
                    s.send("WELCOME".encode())
                    shared_dict["state"] = "WAITING_WELCOME"
                    
                elif shared_dict["state"] == "NEXTLEVEL":
                    s.send("READYTOPLAY".encode())
                    shared_dict["state"] = "WAITING_NEXTLEVEL"

                elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) > 0:
                    if width/5 <= mouse[0] <= width/5+120 and height/5 <= mouse[1] <= height/5+100: 
                        s.send("ASK_REFOCUS".encode())
                        shared_dict["state"] = "ASK_REFOCUS" 
                    else:
                        tosend = "PLAY " +  str(shared_dict["cards"][0])
                        s.send(tosend.encode())
                        shared_dict["lastplay"] = shared_dict["cards"][0]
                        shared_dict["cards"] = shared_dict["cards"][1:]
                
                elif shared_dict["state"] == "MISTAKE":
                    s.send("MISTAKE".encode())
                    shared_dict["state"] = "WAITING_MISTAKE"
                
                elif shared_dict["state"] == "REFOCUS":
                    s.send("REFOCUS".encode())
                    shared_dict["state"] = "WAITING_REFOCUS"



        mouse = pygame.mouse.get_pos() 

        print(shared_dict["state"])
        if shared_dict["state"] == "WELCOME":
            screen.fill((231,84,128))  
            text = font.render("LEVEL "+ str(shared_dict["level"]+1), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
                
            pygame.display.flip()
        if shared_dict["state"] == "WAITING_WELCOME":
            screen.fill((255,182,193)) 
            text = font.render("LEVEL "+ str(shared_dict["level"]+1), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
                
            pygame.display.flip()
        
        elif shared_dict["state"] == "NEXTLEVEL":
            screen.fill((15,170,240)) 
            text = font.render("LEVEL "+ str(shared_dict["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, (screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
            pygame.display.flip()
        
        elif shared_dict["state"] == "WAITING_NEXTLEVEL":
            screen.fill((151,214,242)) 
            text = font.render("LEVEL "+ str(shared_dict["level"]), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, (screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
            pygame.display.flip()

        elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) > 0:
            screen.fill((255,255,255)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))

            if width/5 <= mouse[0] <= width/5+120 and height/5 <= mouse[1] <= height/5+100: 
                pygame.draw.rect(screen,(178,223,138) ,[width/5,height/5,120,100]) 
                
            else: 
                pygame.draw.rect(screen,(51,160,44) ,[width/5,height/5,120,100])
                
            text = smallfont.render('refocus' , True , (0,0,0) )
            screen.blit(text , (width/5+10,height/5+30))  
            pygame.display.flip()

        elif shared_dict["state"]  == "GAME" and len(shared_dict["cards"]) == 0:
            screen.fill((200,200,200)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()
        
        elif shared_dict["state"]  == "MISTAKE":
            screen.fill((223,28,28)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()
        
        elif shared_dict["state"]  == "WAITING_MISTAKE":
            screen.fill((242,110,110)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        elif shared_dict["state"]  == "REFOCUS":
            screen.fill((51,160,44)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        elif shared_dict["state"]  == "WAITING_REFOCUS":
            screen.fill((178,223,138)) 
            cards_text = font.render(str(shared_dict["cards"]), True, (0, 0, 0))
            screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()


        if shared_dict["state"] == "GAMEOVER":
            screen.fill((255,140,0)) 
            text = font.render("GAME OVER", True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
        