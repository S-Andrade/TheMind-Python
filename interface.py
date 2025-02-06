import pygame

def main():
    # initializing the constructor 
    pygame.init() 

    screen_info = pygame.display.Info()
    width = screen_info.current_w
    height = screen_info.current_h - 25
    screen = pygame.display.set_mode((width, height))
    # screen resolution 
    
    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35) 

    width = screen.get_width() 
    height = screen.get_height()

    font = pygame.font.SysFont("calibri",80)
    smallfont = pygame.font.SysFont('Corbel',35)
    sfont = pygame.font.SysFont("calibri",40)

    image = pygame.image.load("arrow.png").convert_alpha()
    image = pygame.transform.scale(image, (150, 150))


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        screen.fill((255, 255, 255))
                
        text = font.render(str(55), True, (0, 0, 0))
        screen.blit(text, text.get_rect(center = screen.get_rect().center))
        liv = font.render("LIVES: "+ str(2), True, (0, 0, 0))
        screen.blit(liv, (10,10))
        lev = font.render("LEVEL: "+ str(1), True, (0, 0, 0))
        screen.blit(lev, (10,80))
        pl0 = sfont.render("Player0: "+ str(10), True, (0, 0, 0))
        screen.blit(pl0, (10, height-50))
        pl1 = sfont.render("Player1: "+ str(10), True, (0, 0, 0))
        screen.blit(pl1, (width-200,height-50))
        r = sfont.render("Player2: "+ str(10), True, (0, 0, 0))
        screen.blit(r, (width/2-50, 10))

        angle = -90

        # Rotate image
        rotated_image = pygame.transform.rotate(image, angle)

        # Get new rect and center it
        rect = rotated_image.get_rect(center=(width/2, height/4))  # Adjust center position

        # Blit (draw) the rotated image
        screen.blit(rotated_image, rect.topleft)

        pygame.display.flip()


main()