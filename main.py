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

# Disk sizes and colors
disk_data = {
    "purple": {"size": 200, "color": PURPLE},
    "red": {"size": 170, "color": RED},
    "blue": {"size": 140, "color": BLUE},
    "green": {"size": 110, "color": GREEN},
    "yellow": {"size": 80, "color": YELLOW},
    "orange": {"size": 60, "color": ORANGE},
    "pink": {"size":30, "color": PINK}
}

# Poles (A, B, C) are represented as stacks (bottom to top)
poles = {
    "A": ["purple", "red", "blue", "green", "yellow", "orange", "pink"],
    "B": [],
    "C": []
}

# Pole positions on the screen
pole_positions = {
    "A": 150,
    "B": 400,
    "C": 650
}

# Function to draw the poles
def draw_poles():
    pygame.draw.line(screen, BLACK, [150, 400], [150, 100], 10)
    pygame.draw.line(screen, BLACK, [400, 400], [400, 100], 10)
    pygame.draw.line(screen, BLACK, [650, 400], [650, 100], 10)
    pygame.draw.line(screen, BLACK, [146, 400], [655, 400], 10)

# Function to draw disks on the screen
def draw_disks():
    for pole in poles:
        x = pole_positions[pole]  # Get the X position of the pole
        for i, disk in enumerate(poles[pole]):
            y = 370 - (i * 30)  # Position disks correctly on the pole
            width = disk_data[disk]["size"]
            color = disk_data[disk]["color"]
            pygame.draw.rect(screen, color, [x - (width // 2), y, width, 20])

def draw_components():
    draw_poles()
    draw_disks()
    draw_text("Press SPACE to pause", font, BLACK, 250, 500)

def home_page():
    #background of the game
    background = pygame.image.load("images/bg.jpg")
    bg_resized = pygame.transform.scale(background, (1000, 600))
    screen.blit(bg_resized, (0, 0))

    # display game name
    draw_text("Towers of Hanoi", heading, BLACK, 200, 100)

#initialize variables
game_started = False

# Variable to control the game loop
running = True

# Main game loop
while running:

    if not game_started:
        home_page()

        # display buttons
        if start_button.draw():
            #if the start button is pressed then the game starts
            game_started = True 

        if exit_button.draw():
            #if the exit button is pressed then the game closes
            running = False

    if game_started:
        #if the game starts then draw the components
        draw_components()
    
    # Event handling loop
    for event in pygame.event.get():
        # Check if the user closes the window
        if event.type == pygame.QUIT:
            running = False  # Exit the loop and close the game

    # Update the display to reflect any changes
    pygame.display.update()