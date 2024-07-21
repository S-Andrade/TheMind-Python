import time
import csv
from ElmoV2API import ElmoV2API
import subprocess
import pygame
from playsound import playsound
import sys

def main(filename):
    pygame.init()
 
    screen = pygame.display.set_mode((1500, 800))
    
    pygame.display.set_caption('SVM')
    clock = pygame.time.Clock()

    import zmq
    port = "5000"

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect ("tcp://localhost:%s" % port)
    topic_filter = b'HeadPose:'
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

    data = {"Left":[], "Right":[], "Down":[], "Front":[]}
    for j in [0,1]:
        for pose in data.keys():
            print(pose)
            pygame.event.get()
            screen.fill((255,255,255))
            font = pygame.font.SysFont("calibri",80)
            image = pose + ".png"
            imp = pygame.image.load(image).convert()
            imp = pygame.transform.scale(imp, (500, 500))
            screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
            pygame.display.flip()
            file = pose+".mp3"
            playsound(file)

            counter = 4
            text = font.render(str(counter), True, (0, 0, 0))

            timer_event = pygame.USEREVENT+1
            pygame.time.set_timer(timer_event, 1000)

            run = True
            while run:
                clock.tick(60)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    elif event.type == timer_event:
                        counter -= 1
                        if counter != 0:
                            text = font.render(str(counter), True, (0, 0, 0))
                            screen.fill((255,255,255))
                            image = pose + ".png"
                            imp = pygame.image.load(image).convert()
                            imp = pygame.transform.scale(imp, (500, 500))
                            screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                            #text_rect = text.get_rect(center = screen.get_rect().center)
                            screen.blit(text, (screen.get_rect().centerx -20 ,screen.get_rect().centery + 150))
                            pygame.display.flip()
                            playsound("bop.mp3")
                        if counter == 0:
                            run = False 
                            screen.fill((255,255,255))
                            image = pose + ".png"
                            imp = pygame.image.load(image).convert()
                            imp = pygame.transform.scale(imp, (500, 500))
                            screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                            pygame.display.flip()
                            playsound("bip.mp3")             
                

            if pose == "Left":
                #playsound("blue.wav")
                playsound("blue.mp3")
                text = font.render("Blue cube", True, (0, 0, 0))
                screen.fill((255,255,255))
                image = pose + ".png"
                imp = pygame.image.load(image).convert()
                imp = pygame.transform.scale(imp, (500, 500))
                screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                screen.blit(text, (screen.get_rect().centerx - 150 ,screen.get_rect().centery + 150))
                pygame.display.flip()

            if pose == "Right":
                #playsound("pink.wav")
                playsound("pink.mp3")
                text = font.render("Pink cube", True, (0, 0, 0))
                screen.fill((255,255,255))
                image = pose + ".png"
                imp = pygame.image.load(image).convert()
                imp = pygame.transform.scale(imp, (500, 500))
                screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                screen.blit(text, (screen.get_rect().centerx - 200 ,screen.get_rect().centery + 150))
                pygame.display.flip()
            if pose == "Down":
                #playsound("banana.wav")
                playsound("banana.mp3")
                text = font.render("Banana sticker", True, (0, 0, 0))
                screen.fill((255,255,255))
                image = pose + ".png"
                imp = pygame.image.load(image).convert()
                imp = pygame.transform.scale(imp, (500, 500))
                screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                screen.blit(text, (screen.get_rect().centerx - 225 ,screen.get_rect().centery + 150))
                pygame.display.flip()
            if pose == "Front":
                #playsound("pink.wav")
                playsound("pink.mp3")
                screen.fill((255,255,255))
                textFront = font.render("FRONT", True, (0, 0, 0))
                screen.blit(textFront,(screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
                pygame.draw.circle(screen, (222, 49, 99), (200, 200), 100)
                pygame.display.flip()


            i = 0
            data_pose = []
            while i < 450:
                        
                if i == 149:
                    if pose == "Left":
                        #playsound("red.wav")
                        playsound("red.mp3")
                        text = font.render("Red cubo", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 150 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Right":
                        #playsound("green.wav")
                        playsound("green.mp3")
                        text = font.render("Green cubo", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 200 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Down":
                        #playsound("watermalon.wav")
                        playsound("watermellon.mp3")
                        text = font.render("Watermellon sticker", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 300 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Front":
                        #playsound("blue.wav")
                        playsound("blue.mp3")
                        screen.fill((255,255,255))
                        textFront = font.render("FRONT", True, (0, 0, 0))
                        screen.blit(textFront,(screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
                        pygame.draw.circle(screen, (0, 150, 255), (750, 400), 100)
                        pygame.display.flip()
                     
                if i == 299:
                    if pose == "Left":
                        #playsound("yellow.wav")
                        playsound("yellow.mp3")
                        text = font.render("Yellow cubo", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 150 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Right":
                        #playsound("orange.wav")
                        playsound("orange.mp3")
                        text = font.render("Orange cubo", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 225 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Down":
                        #playsound("chery.wav")
                        playsound("chery.mp3")
                        text = font.render("Chery sticker", True, (0, 0, 0))
                        screen.fill((255,255,255))
                        image = pose + ".png"
                        imp = pygame.image.load(image).convert()
                        imp = pygame.transform.scale(imp, (500, 500))
                        screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
                        screen.blit(text, (screen.get_rect().centerx - 200 ,screen.get_rect().centery + 150))
                        pygame.display.flip()
                    if pose == "Front":
                        #playsound("green.wav")
                        playsound("green.mp3")
                        screen.fill((255,255,255))
                        textFront = font.render("FRONT", True, (0, 0, 0))
                        screen.blit(textFront,(screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
                        pygame.draw.circle(screen, (0, 128, 0), (1300, 600), 100)
                        pygame.display.flip()
                
                head_pose = socket.recv()
                head_pose = head_pose.decode()
                head_pose = head_pose[9:].split(', ')
                head_pose = [hp.replace(',', '.') for hp in head_pose]
                X = float(head_pose[0])
                Y = float(head_pose[1])
                Z = float(head_pose[2])

                pitch = float(head_pose[3])
                yaw = float(head_pose[4])
                roll = float(head_pose[5])
                data_pose.append([X, Y, Z, pitch, yaw, roll])
                i+=1
                time.sleep(0.01)

            data[pose] += data_pose
            playsound("bip.mp3")
            text = font.render("Done", True, (0, 0, 0))
            screen.fill((255,255,255))
            image = pose + ".png"
            imp = pygame.image.load(image).convert()
            imp = pygame.transform.scale(imp, (500, 500))
            screen.blit(imp,(screen.get_rect().centerx - 250,screen.get_rect().centery - 400))
            screen.blit(text, (screen.get_rect().centerx - 100 ,screen.get_rect().centery + 150))
            pygame.display.flip()
            time.sleep(3)

    filename = "data\\" + filename + ".tsv"
    with open(filename, 'w', encoding='utf8', newline='') as tsv_file:
                tsv_writer = csv.writer(tsv_file, delimiter='\t', lineterminator='\n')
                for pose in data.keys():
                      tsv_writer.writerow([pose])
                      for line in data[pose]:
                            tsv_writer.writerow(line)


if __name__ == '__main__':
    main(sys.argv[1])