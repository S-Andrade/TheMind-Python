import pygame
import time

pygame.init() 
    
# screen resolution 
res = (720,720) 
screen = pygame.display.set_mode(res) 
font = pygame.font.SysFont("calibri",80)
smallfont = pygame.font.SysFont('Corbel',35) 

width = screen.get_width() 
height = screen.get_height()
mouse = pygame.mouse.get_pos() 


screen.fill((255,255,255)) 
cards_text = font.render(str([1,2,5]), True, (0, 0, 0))
screen.blit(cards_text, cards_text.get_rect(center = screen.get_rect().center))

if width/5 <= mouse[0] <= width/5+140 and height/5 <= mouse[1] <= height/5+40: 
    pygame.draw.rect(screen,(0,100,0) ,[width/5,height/5,120,100]) 
    
else: 
    pygame.draw.rect(screen,(144,238,144) ,[width/5,height/5,120,100])
    
text = smallfont.render('refocus' , True , (0,0,0) )
screen.blit(text , (width/5+10,height/5+30))  
pygame.display.flip()

time.sleep(5)