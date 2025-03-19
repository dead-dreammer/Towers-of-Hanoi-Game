import pygame

import pygame

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
RED = (250, 0, 0)
GREEN = (0, 250, 0)
BLUE = (0, 0, 250)
PURPLE = (125, 0, 125)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
PINK = (255, 20, 147)

# Create the game window with dimensions 800x600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Towers of Hanoi")
icon = pygame.image.load("images/ring.png")
pygame.display.set_icon(icon)

# font 
font = pygame.font.SysFont("arialblack", 25)
heading = pygame.font.SysFont("arialblack", 45)

# function for rendering font
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Button class to create button instances
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False # start off each button with not clicked

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        # Draw the button image
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
        # Check if the mouse is over the button
        if self.rect.collidepoint(pos):

            # Check if the left mouse button is pressed
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True  # Button was just clicked
            
        # Reset click state when mouse button is released
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action
    
#load button images
start_img = pygame.image.load("buttons/start.png").convert_alpha()
exit_img = pygame.image.load("buttons/exit.png").convert_alpha()

# create the start and exit button
start_button = Button(100, 200, start_img, 0.5)
exit_button = Button(450, 225, exit_img, 0.4)


# Variable to control the game loop
running = True

# Main game loop
while running:
    
    #background of the game
    background = pygame.image.load("images/bg.jpg")
    bg_resized = pygame.transform.scale(background, (1000, 600))
    screen.blit(bg_resized, (0, 0))

    # display game name
    draw_text("Towers of Hanoi", heading, BLACK, 200, 100)

    # display buttons
    start_button.draw()

    if exit_button.draw():
        running = False
    
    # Event handling loop
    for event in pygame.event.get():
        # Check if the user closes the window
        if event.type == pygame.QUIT:
            running = False  # Exit the loop and close the game

    # Update the display to reflect any changes
    pygame.display.update()