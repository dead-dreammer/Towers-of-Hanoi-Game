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

# Track selected disk and its original pole
selected_disk = None
selected_pole = None

# Function to check if a move is valid (smaller disk on top)
def can_move(disk, target_pole):
    if not poles[target_pole]:  # If target pole is empty, allow move
        return True
    top_disk = poles[target_pole][-1]  # Get the top disk
    return disk_data[disk]["size"] < disk_data[top_disk]["size"]

# Function to handle disk movement
def move_disk(from_pole, to_pole):

    if from_pole and to_pole and poles[from_pole]:  # Ensure there's a disk to move
        disk = poles[from_pole][-1]  # Get the top disk
        if can_move(disk, to_pole):  # Check if move is valid
            start_x = pole_positions[from_pole]  # Get starting X position
            end_x = pole_positions[to_pole]  # Get target X position
            y = 370 - (len(poles[from_pole]) * 30)  # Get current Y position

            poles[from_pole].pop()  # Remove from old pole
            
            # Move disk upwards (to lift it)
            for step in range(10):
                screen.fill(WHITE)  
                draw_components()
                pygame.draw.rect(screen, disk_data[disk]["color"], [start_x - (disk_data[disk]["size"] // 2), y - (step * 10), disk_data[disk]["size"], 20])
                pygame.display.update()
                pygame.time.delay(30)  # Small delay for smooth animation

            # Move disk sideways (to the new pole)
            for step in range(10):
                screen.fill(WHITE)
                draw_components()
                new_x = start_x + (end_x - start_x) * (step / 10)
                pygame.draw.rect(screen, disk_data[disk]["color"], [new_x - (disk_data[disk]["size"] // 2), y - 100, disk_data[disk]["size"], 20])
                pygame.display.update()
                pygame.time.delay(30)

            # Move disk downwards (onto the new pole)
            for step in range(10):
                screen.fill(WHITE)
                draw_components()
                new_y = (370 - (len(poles[to_pole]) * 30)) - (100 - step * 10)
                pygame.draw.rect(screen, disk_data[disk]["color"], [end_x - (disk_data[disk]["size"] // 2), new_y, disk_data[disk]["size"], 20])
                pygame.display.update()
                pygame.time.delay(30)

            poles[to_pole].append(disk)  # Add to new pole

            return True
    return False

# Function to get pole based on mouse click position
def get_pole_from_x(x):
    if 100 <= x <= 200:
        return "A"
    elif 350 <= x <= 450:
        return "B"
    elif 600 <= x <= 700:
        return "C"
    return None

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
    screen.fill(WHITE)  # Clear screen

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

        
        # Handle mouse click (pick up or drop disk)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_pole = get_pole_from_x(mouse_x)

            if clicked_pole:  # If a pole was clicked
                if selected_disk is None and poles[clicked_pole]:  # Pick up a disk
                    selected_disk = poles[clicked_pole][-1]
                    selected_pole = clicked_pole
                    print(f"🎯 Picked up {selected_disk} from {selected_pole}")

                elif selected_disk is not None:  # Drop the disk
                    if move_disk(selected_pole, clicked_pole):
                        print(f"✅ Moved {selected_disk} to {clicked_pole}")
                    else:
                        draw_text(f"❌ Invalid move for {selected_disk} to {clicked_pole}", font, BLACK, 100, 400)
                    selected_disk = None
                    selected_pole = None

    # Update the display to reflect any changes
    pygame.display.update()