import pygame

def main():
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 

    level = 8
    cards = [1, 3, 25, 30, 40, 50, 67, 77, 80, 99]
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 50
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",200)
    fontCardList = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Regular.ttf",100)
    fontbuttons = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",70)

    button_play = pygame.Rect(width/2-100,height/2-50,200,100)
    button_refocus = pygame.Rect(width/6,height/6,300,100)
   
    run = True

    while run:
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255,255,255)) 
        cards_text = fontCardList.render(str(cards), True, (0, 0, 0))
        text_width, text_height = cards_text.get_size()
        x = (width - text_width) // 2
        if x < 0:
            x = 0
        screen.blit(cards_text, (x ,height/1.5))

        
        pygame.draw.rect(screen,(51,160,44) , button_refocus)
        
        text = fontbuttons.render('refocus' , True , (0,0,0) )
        screen.blit(text , (width/6+20,height/6)) 

        pygame.draw.rect(screen,(255, 193, 7) , button_play)

        text = fontbuttons.render('play' , True , (0,0,0) )
        screen.blit(text , (width/2-70,height/2-50)) 
        
        pygame.display.flip()

main()