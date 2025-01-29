import pygame
import time

pygame.init() 


screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Set up the screen to fullscreen with the screen width and height
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont("calibri",80)
smallfont = pygame.font.SysFont('Corbel',35)
sfont = pygame.font.SysFont("calibri",40)

# Card properties
card_width, card_height = 100, 150
start_pos = (10, 10)  # Top-left corner
target_pos = (width // 2 - card_width // 2, height // 2 - card_height // 2)
current_pos = list(start_pos)

# Movement speed (fraction of the distance per frame)
speed = 0.05

# Load card images (placeholders: colored rectangles)
center_card_color = (0, 0, 255)  # Blue for the stationary card
moving_card_color = (255, 0, 0)  # Red for the moving card

center_card_surface = pygame.Surface((card_width, card_height))
center_card_surface.fill(center_card_color)

moving_card_surface = pygame.Surface((card_width, card_height))
moving_card_surface.fill(moving_card_color)

clock = pygame.time.Clock()
running = True

last_position = [-1,-1]
count_position = 

while running:
    screen.fill((255,255,255)) 

    text = font.render(str(20), True, (0, 0, 0))
    screen.blit(center_card_surface, target_pos)

    lives = font.render("LIVES: "+ str(2), True, (0, 0, 0))
    screen.blit(lives, (10,10))
    level = font.render("LEVEL: "+ str(9), True, (0, 0, 0))
    screen.blit(level, (10,80))
    p0 = sfont.render("Player0: "+ str(1), True, (0, 0, 0))
    screen.blit(p0, (10,height-50))
    p1 = sfont.render("Player1: "+ str(10), True, (0, 0, 0))
    screen.blit(p1, (width-200,height-50))
    r = sfont.render("Player2: "+ str(10), True, (0, 0, 0))
    screen.blit(r, ((width/2)-100, 15))
    pygame.display.flip()


    # Linear interpolation for smooth movement
    current_pos[0] += (target_pos[0] - current_pos[0]) * speed
    current_pos[1] += (target_pos[1] - current_pos[1]) * speed
    # Draw the moving card on top
    screen.blit(moving_card_surface, current_pos)
    
    # Update display
    pygame.display.flip()
    print(current_pos)
    if current_pos[0] == last_position[0] and current_pos[1] == last_position[1]:
        running = False

    last_position = current_pos
    print(last_position)
    # Cap the frame rate
    clock.tick(60)

time.sleep(2)




"""import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Card Movement Example")

# Card properties
card_width, card_height = 100, 150
start_pos = (10, 10)  # Top-left corner
target_pos = (screen_width // 2 - card_width // 2, screen_height // 2 - card_height // 2)
current_pos = list(start_pos)

# Movement speed (fraction of the distance per frame)
speed = 0.05

# Load card images (placeholders: colored rectangles)
center_card_color = (0, 0, 255)  # Blue for the stationary card
moving_card_color = (255, 0, 0)  # Red for the moving card

center_card_surface = pygame.Surface((card_width, card_height))
center_card_surface.fill(center_card_color)

moving_card_surface = pygame.Surface((card_width, card_height))
moving_card_surface.fill(moving_card_color)

# Main loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Linear interpolation for smooth movement
    current_pos[0] += (target_pos[0] - current_pos[0]) * speed
    current_pos[1] += (target_pos[1] - current_pos[1]) * speed

    # Clear screen
    screen.fill((30, 30, 30))

    # Draw the center card first (stationary card)
    screen.blit(center_card_surface, target_pos)

    # Draw the moving card on top
    screen.blit(moving_card_surface, current_pos)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

"""