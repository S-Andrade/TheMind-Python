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
   
    run = True

    while run:
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False

        screen.fill((223,28,28))
        cards_text = fontCardList.render(str(cards), True, (0, 0, 0))
        text_width, text_height = cards_text.get_size()
        x = (width - text_width) // 2
        if x < 0:
            x = 0
        screen.blit(cards_text, (x,screen.get_rect().centery + 200))
        pygame.display.flip()


main()