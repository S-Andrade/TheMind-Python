import pygame

def main():
    global clients, p0, p1, p2, gameState, card_played, lives, topPile, level, player_played 

    level = 8
    pygame.init() 

    # Get screen info
    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 50
    screen = pygame.display.set_mode((width, height))

    font = pygame.font.Font("..\\tt_rounds_neue\TT Rounds Neue Trial Black.ttf",200)
   
    run = True

    while run:
        for event in pygame.event.get():
             
            if event.type == pygame.QUIT:
                run = False

        screen.fill((255,140,0)) 
        text = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center = screen.get_rect().center))
        pygame.display.flip()


main()