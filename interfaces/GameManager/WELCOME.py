import pygame

def main():
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 

    level = 8
    lives = 3
    p0 = "GAME"
    p1 = "GAME"
    p2 = "GAME"
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 50
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",200)
    fontinfo = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Regular.ttf",50)
    fonttoppile = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",70)
    fontinfocards = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",80)

    image_hand = pygame.image.load("..\\..\\hand.png").convert_alpha()
    image_hand = pygame.transform.scale(image_hand, (150, 150))
   
    run = True

    while run:
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False

        screen.fill((231,84,128))
        text = font.render("LEVEL "+ str(level), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center = screen.get_rect().center))
        liv = fontinfo.render("LIVES: "+ str(lives), True, (0, 0, 0))
        screen.blit(liv, (10,10))
        pl0x = 40
        pl0y = height-100
        pl0 = fontinfo.render("P0: ", True, (0, 0, 0)) 
        screen.blit(pl0,(pl0x,pl0y))
        pl01 = fontinfocards.render("10", True, (0, 0, 0))
        screen.blit(pl01,(pl0x + pl0.get_width(),pl0y-30))
        pl02 = fontinfo.render(" cards", True, (0, 0, 0))
        screen.blit(pl02,(pl0x + pl0.get_width() + pl01.get_width(),pl0y))
        
        pl1x = width-350
        pl1y = height-100
        pl1 = fontinfo.render("P1: ", True, (0, 0, 0)) 
        screen.blit(pl1,(pl1x,pl1y))
        pl11 = fontinfocards.render("10", True, (0, 0, 0))
        screen.blit(pl11,(pl1x + pl1.get_width(),pl1y-30))
        pl12 = fontinfo.render(" cards", True, (0, 0, 0))
        screen.blit(pl12,(pl1x + pl1.get_width() + pl11.get_width(),pl1y))

        pl2x = width/2-150
        pl2y = 40
        pl2 = fontinfo.render("P2: ", True, (0, 0, 0)) 
        screen.blit(pl2,(pl2x,pl2y))
        pl21 = fontinfocards.render("10", True, (0, 0, 0))
        screen.blit(pl21,(pl2x + pl2.get_width(),pl2y-30))
        pl22 = fontinfo.render(" cards", True, (0, 0, 0))
        screen.blit(pl22,(pl2x + pl2.get_width() + pl21.get_width(),pl2y))

        if p0 == "GAME":
            angle = -45
            rotated_image = pygame.transform.rotate(image_hand, angle)
            rect = rotated_image.get_rect(center=(width/4, height*(3/4)))
            screen.blit(rotated_image, rect.topleft)

        if p1 == "GAME":
            angle = 45
            rotated_image = pygame.transform.rotate(image_hand, angle)
            rect = rotated_image.get_rect(center=(width*(3/4), height*(3/4)))
            screen.blit(rotated_image, rect.topleft)
            
        if p2 == "GAME":
            angle = -180
            rotated_image = pygame.transform.rotate(image_hand, angle)
            rect = rotated_image.get_rect(center=(width/2, height/4))
            screen.blit(rotated_image, rect.topleft)
        
        pygame.display.flip()


main()