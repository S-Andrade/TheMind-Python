import pygame
import time


pygame.init()
 
screen = pygame.display.set_mode((1500, 800))

pygame.display.set_caption('SVM')

font = pygame.font.SysFont("calibri",80)



screen.fill((255,255,255))
textFront = font.render("FRONT", True, (0, 0, 0))
screen.blit(textFront,(screen.get_rect().centerx - 100,screen.get_rect().centery - 200))
pygame.draw.circle(screen, (222, 49, 99), (200, 200), 100)
pygame.draw.circle(screen, (0, 150, 255), (750, 400), 100)
pygame.draw.circle(screen, (0, 128, 0), (1300, 600), 100)
pygame.display.flip()

time.sleep(3)