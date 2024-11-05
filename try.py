import pygame
import time

pygame.init() 
res = (720,720) 
screen = pygame.display.set_mode(res) 
font = pygame.font.SysFont("calibri",80)
smallfont = pygame.font.SysFont('Corbel',35)
sfont = pygame.font.SysFont("calibri",40)
screen.fill((51,160,44)) 
text = font.render(str(0), True, (0, 0, 0))
screen.blit(text, text.get_rect(center = screen.get_rect().center))
lives = font.render("LIVES: "+ str(1), True, (0, 0, 0))
screen.blit(lives, (10,10))
level = font.render("LEVEL: "+ str(1), True, (0, 0, 0))
screen.blit(level, (10,80))

p0 = sfont.render("Player0: "+ str(1) + " " + str([23,44]), True, (0, 0, 0))
screen.blit(p0, (10,600))
p1 = sfont.render("Player1: "+ str(1) + " " + str([23,44]), True, (0, 0, 0))
screen.blit(p1, (10,640))
r = sfont.render("Robot: "+ str(1) + " " + str([23,44]), True, (0, 0, 0))
screen.blit(r, (10, 680))
pygame.display.flip()

time.sleep(5)