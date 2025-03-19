import pygame

import pygame

# Initialize pygame
pygame.init()

# Create the game window with dimensions 800x600
screen = pygame.display.set_mode((800, 600))

# Variable to control the game loop
running = True

# Main game loop
while running:
    
    # Event handling loop
    for event in pygame.event.get():
        # Check if the user closes the window
        if event.type == pygame.QUIT:
            running = False  # Exit the loop and close the game

    # Update the display to reflect any changes
    pygame.display.update()