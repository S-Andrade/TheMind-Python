import pygame
import sys

pygame.init()

# Get screen info
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h - 25
screen = pygame.display.set_mode((width, height))

# Fonts
font = pygame.font.SysFont("calibri", 80)
smallfont = pygame.font.SysFont('Corbel', 35)
sfont = pygame.font.SysFont("calibri", 40)

# Card properties
card_width, card_height = 100, 150

# Define the target position (center of the screen)
target_pos = (width // 2 - card_width // 2, height // 2 - card_height // 2)

# Movement speed (fraction of the distance per frame)
speed = 0.05

# Create card surfaces
center_card_color = (0, 0, 255)  # Blue card in center
moving_card_color = (255, 0, 0)  # Red moving card

center_card_surface = pygame.Surface((card_width, card_height))
center_card_surface.fill(center_card_color)

moving_card_surface = pygame.Surface((card_width, card_height))
moving_card_surface.fill(moving_card_color)

# Text to overlay on cards
moving_card_text = font.render(str(80), True, (255, 255, 255))
center_card_text = font.render(str(90), True, (255, 255, 255))

# Main loop
clock = pygame.time.Clock()
run = True

while run:
    # Get user input for card movement
    user_input = input("Enter movement type (0 - center top, 1 - left bottom, 2 - right bottom): ")
    
    # Validate the user input
    if user_input not in ["0", "1", "2"]:
        print("Invalid input. Please enter 0, 1, or 2.")
        continue

    # Convert input to integer
    user_input = int(user_input)
    
    # Set start position based on input
    if user_input == 2:
        start_pos = (width - card_width, height)  # Right bottom corner
    elif user_input == 1:
        start_pos = (0, height)  # Left bottom corner
    elif user_input == 0:
        start_pos = (width // 2 - card_width // 2, 0)  # Center top

    # Set initial position for the moving card
    current_pos = list(start_pos)

    # Main game loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update card position (linear interpolation)
        current_pos[0] += (target_pos[0] - current_pos[0]) * speed
        current_pos[1] += (target_pos[1] - current_pos[1]) * speed

        # Clear screen
        screen.fill((255, 255, 255))

        # Draw the stationary center card first
        screen.blit(center_card_surface, target_pos)

        # Blit text onto the center card
        center_card_text_rect = center_card_text.get_rect(center=(target_pos[0] + card_width // 2, target_pos[1] + card_height // 2))
        screen.blit(center_card_text, center_card_text_rect)

        # Draw the moving card on top of the stationary card
        screen.blit(moving_card_surface, current_pos)

        # Blit text onto the moving card
        moving_card_text_rect = moving_card_text.get_rect(center=(current_pos[0] + card_width // 2, current_pos[1] + card_height // 2))
        screen.blit(moving_card_text, moving_card_text_rect)

        # Display other text elements
        lives = font.render("LIVES: " + str(2), True, (0, 0, 0))
        screen.blit(lives, (10, 10))
        
        level = font.render("LEVEL: " + str(9), True, (0, 0, 0))
        screen.blit(level, (10, 80))
        
        p0 = sfont.render("Player0: " + str(1), True, (0, 0, 0))
        screen.blit(p0, (10, height - 50))
        
        p1 = sfont.render("Player1: " + str(10), True, (0, 0, 0))
        screen.blit(p1, (width - 200, height - 50))
        
        r = sfont.render("Player2: " + str(10), True, (0, 0, 0))
        screen.blit(r, ((width / 2) - 100, 15))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

        # Stop the inner loop if the card reaches the target position
        if abs(current_pos[0] - target_pos[0]) < 1 and abs(current_pos[1] - target_pos[1]) < 1:
            break  # Exit the inner loop and ask for input again

pygame.quit()
sys.exit()
