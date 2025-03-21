import pygame
import time

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
undo_img = pygame.image.load("buttons/undo.png").convert_alpha()


# create the start and exit button
start_button = Button(100, 200, start_img, 0.5)
exit_button = Button(450, 225, exit_img, 0.4)
undo_button = Button(700, 50, undo_img, 0.1)

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
    global move_count

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
            move_history.append((from_pole, to_pole))  # Save move for undo
            move_count += 1

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

# Track moves (stores tuples of (from_pole, to_pole))
move_history = []
move_count = 0

def undo_move():
    global move_count
    if move_history:  # If there are moves to undo
        last_from, last_to = move_history.pop()  # Get last move
        if poles[last_to]:  # Ensure there's a disk to move back
            disk = poles[last_to].pop()
            poles[last_from].append(disk)  # Move disk back
            move_count -= 1

# Timer variables
start_time = None  # Stores when the game starts
paused_time = 0
game_paused = False

def draw_timer():
    global start_time, paused_time, elapsed_time
    
    if start_time:
        if game_paused:
            # If the game is paused, show the time as it was before the pause
            elapsed_time = paused_time
        else:
            # Calculate the time since the game started or resumed
            elapsed_time = time.time() - start_time + paused_time

        # Draw the timer
        font = pygame.font.Font(None, 36)

        # Convert elapsed time to minutes and seconds
        minutes = int(elapsed_time) // 60
        seconds = int(elapsed_time) % 60

        timer_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, BLACK)
        screen.blit(timer_text, (350, 450))  # Draw timer at the top right

# Function to display a text input box and get user input
def get_user_input(prompt):
    input_box = pygame.Rect(510, 295, 100, 50)
    color_inactive = pygame.Color(BLACK)
    color_active = pygame.Color(RED)
    color = color_inactive
    text = ''
    active = False
    done = False
    clock = pygame.time.Clock()

    pygame.event.clear()  # Clears old events to prevent conflicts

    while not done:

        draw_text(prompt, font, BLACK, 100, 300)
        pygame.draw.rect(screen, color, input_box, 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = True
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN and text.strip().isdigit():
                        return text  # Instead of quitting, return input to the game
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.unicode.isdigit():  # Allow only digits
                        text += event.unicode

        # Render the text inside the input box
        txt_surface = font.render(text, True, BLACK)
        screen.blit(txt_surface, (input_box.x + 40, input_box.y + 10))

        pygame.display.update()
        clock.tick(30)

    return text  # Ensure the function returns input instead of exiting

num_disks = None

def check_disks(num_disks):
    if 3 <= num_disks <= 7:
        poles["A"] = list(disk_data.keys())[:num_disks]  # Set the number of disks
        return True
    
    else:
        draw_text("Invalid input! Enter a number between 3 and 7.", font, RED, 130, 430)
        pygame.display.update()
        time.sleep(1)  # Show the message briefly before retrying
        return False


def draw_components():
    if game_paused:
        screen.fill(WHITE)
        draw_text("Game Paused", heading, BLACK, 250, 250)

    else:
        draw_poles()
        draw_disks()
        draw_timer()
        draw_text("Press SPACE to pause", font, BLACK, 250, 500)

    if undo_button.draw():
        undo_move()

def home_page():
    global bg_resized
    #background of the game
    background = pygame.image.load("images/bg.jpg")
    bg_resized = pygame.transform.scale(background, (1000, 600))
    screen.blit(bg_resized, (0, 0))

    # display game name
    draw_text("Towers of Hanoi", heading, BLACK, 200, 100)

# initialize variables
game_started = False

# Variable to control the game loop
running = True

# Main game loop
while running:
    screen.fill(WHITE)  # Clear screen

    if not game_started:
        home_page()

        # Always show Start and Exit buttons before game starts
        if start_button.draw():

            if num_disks is None:  # Ask for input only when needed
                screen.blit(bg_resized, (0, 0))
                draw_text("Towers of Hanoi", heading, BLACK, 200, 100)
                draw_text("Press Enter to Continue", font, RED, 250, 400)


                temp_input = get_user_input("Enter number of disks (3-7):")
                if temp_input.isdigit():
                    temp_input = int(temp_input)
                    if check_disks(temp_input):  # Only start if input is valid
                        num_disks = temp_input
                        game_started = True
                        start_time = time.time()  # Start timer

                

        if exit_button.draw():
            running = False  # Exit game

    if game_started:
        #if the game starts then draw the components
        draw_components()
    
    # Event handling loop
    for event in pygame.event.get():
        # Check if the user closes the window
        if event.type == pygame.QUIT:
            running = False  # Exit the loop and close the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_paused:
                    # Unpause the game
                    game_paused = False
                    start_time = time.time()  # Reset the start time when resuming
                else:
                    # Pause the game
                    game_paused = True
                    if start_time:  # Only update paused_time if the game has started
                        paused_time += time.time() - start_time  # Add time before pausing to paused_time
                    start_time = None  # Stop the timer when paused

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