import time
import csv
from ElmoV2API import ElmoV2API
import subprocess
import pygame
from playsound import playsound
import sys
import random
import zmq

def main(filename):
    pygame.init()
 
    screen = pygame.display.set_mode((1500, 800))
    
    pygame.display.set_caption('SVM')
    clock = pygame.time.Clock()
    
    port = "5000"

    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    print("Collecting head pose updates...")

    socket.connect ("tcp://localhost:%s" % port)
    topic_filter = b'HeadPose:'
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

    getlabel = {"Left":0, "Right":0, "Down":0, "Front":0}
    data = {"Left":[], "Right":[], "Down":[], "Front":[]}

    gettarget = {"Left":{"PINK CUBE":0, "BLUE CUBE":0,"YELLOW CUBE":0,"LILAC CUBE":0, "previous": ""}, "Right":{"RED CUBE":0, "GREEN CUBE":0,"ORANGE CUBE":0,"WHITE CUBE":0,"previous": ""}, "Down":{"WATERMELLON STICKER":0, "BANANA STICKER":0,"CHERY STICKER":0,"KIWI STICKER":0, "previous": ""}, "Front":{"BLACK DOT":0, "PURPLE DOT":0, "GRAY DOT":0, "BROWN DOT":0, "previous": ""}}

    pygame.event.get()
    screen.fill((255,255,255))
    font = pygame.font.SysFont("calibri",80)

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
                    #text_rect = text.get_rect(center = screen.get_rect().center)
                    screen.blit(text, text.get_rect(center = screen.get_rect().center))
                    pygame.display.flip()
                    playsound("bop.mp3")
                if counter == 0:
                    run = False 
                    screen.fill((255,255,255))
                    text = font.render("START", True, (0, 0, 0))
                    screen.blit(text, text.get_rect(center = screen.get_rect().center))
                    pygame.display.flip()
                    playsound("bip.mp3")       

    i = 0
    while i < 32:
        poses = [label for label, value in getlabel.items() if value < 8]
        pose = random.choice(poses)
        getlabel[pose] += 1
        targets = [target for target,value in gettarget[pose].items() if target != "previous" and target != gettarget[pose]["previous"] and value < 2]
        if len(targets) == 0:
            targets = [target for target,value in gettarget[pose].items() if target != "previous" and value < 2]
        target = random.choice(targets)
        gettarget[pose][target] += 1
        gettarget[pose]["previous"] = target

        print(pose + " > " + target)

        if "DOT" in target:
            screen.fill((255,255,255))
            if target == "PURPLE DOT":
                pygame.draw.circle(screen, (148,0,211), (random.randint(200,1300), random.randint(200, 600)), 100)
            if target == "BLACK DOT":
                screen.fill((255,255,255))
                pygame.draw.circle(screen, (0, 0, 0), (random.randint(200,1300), random.randint(200, 600)), 100)
            if target == "GRAY DOT":
                pygame.draw.circle(screen, (105,105,105), (random.randint(200,1300), random.randint(200, 600)), 100)
            if target == "BROWN DOT":
                pygame.draw.circle(screen, (123, 63, 0), (random.randint(200,1300), random.randint(200, 600)), 100)
            pygame.display.flip()

        else:
            screen.fill((255,255,255))
            text = font.render(target, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            pygame.display.flip()

        file = target.replace(" ", "") + ".mp3"

        playsound(file)
        
        data_pose = []
        j = 0
        while j < 150:
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
            j+=1
            time.sleep(0.01)

        data[pose] += data_pose
        i+=1

        p = [(p, len(v)) for p,v in data.items()]
        print(p)
    
    playsound("bip.mp3")
    screen.fill((255,255,255))
    text = font.render("DONE", True, (0, 0, 0))
    screen.blit(text, text.get_rect(center = screen.get_rect().center))
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