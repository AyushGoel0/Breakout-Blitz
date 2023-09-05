import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (800, 600)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 8

def display_credits():
    with open("CREDITS.txt", "r") as file:
        credits_text = file.read()

    # Split the text into individual lines
    credits_lines = credits_text.split("\n")

    # Clear the screen
    screen.fill(BLACK)

    # Create a font for displaying text
    credits_font = pygame.font.Font(None, 24)

    # Y position for rendering each line
    y_position = 50

    # Render and display each line of text
    for line in credits_lines:
        credits_rendered = credits_font.render(line, True, WHITE)
        screen.blit(credits_rendered, (5, y_position))
        y_position += credits_rendered.get_height() + 5  # Add some space between lines

    # Update the display
    pygame.display.flip()

    # Wait for the player to close the credits screen
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press 'Esc' to close the credits screen
                    return


# Set up the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Bouncing Ball Game')

# Simple function to draw text on the screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

# Bricks properties
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_GAP = 10
BRICK_ROWS = 5
BRICK_COLS = 8


# ...
# Sound effects
brick_hit_sound = pygame.mixer.Sound("Sounds/brick_hit.wav")
paddle_hit_sound = pygame.mixer.Sound("Sounds/paddle_hit.wav")
game_over_sound = pygame.mixer.Sound("Sounds/game_over.wav")
game_completed_sound = pygame.mixer.Sound("Sounds/game_completed.wav")

# Function to create bricks
def create_bricks(rows, cols):
    bricks = []
    for row in range(rows):
        for col in range(cols):
            brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
            bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks



# Function to load sounds
def load_sounds():
    pygame.mixer.Sound("Sounds/brick_hit.wav")
    pygame.mixer.Sound("Sounds/paddle_hit.wav")
    pygame.mixer.Sound("Sounds/game_over.wav")
    pygame.mixer.Sound("Sounds/game_completed.wav")

# Game loop
def start_game():
    print("Entering game loop...")
    ball_x = WINDOW_SIZE[0] // 2
    ball_y = WINDOW_SIZE[1] // 2
    ball_speed_x = BALL_SPEED_X
    ball_speed_y = BALL_SPEED_Y

    paddle_x = WINDOW_SIZE[0] // 2 - PADDLE_WIDTH // 2
    paddle_y = WINDOW_SIZE[1] - PADDLE_HEIGHT
    paddle_speed = 0

    clock = pygame.time.Clock()

    paused = False

    

    # Create bricks for each level
    levels = [
        create_bricks(BRICK_ROWS, BRICK_COLS),
        create_bricks(BRICK_ROWS - 1, BRICK_COLS - 1),
        create_bricks(BRICK_ROWS - 2, BRICK_COLS - 2)
    ]

    current_level = 0
    bricks = levels[current_level]

    # Score and lives
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)

    # Game loop

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_speed = -PADDLE_SPEED
                elif event.key == pygame.K_RIGHT:
                    paddle_speed = PADDLE_SPEED
                elif event.key == pygame.K_p:  # Press 'P' to pause/unpause the game
                    paused = not paused
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    paddle_speed = 0

        if not paused:
            # Update ball position
            ball_x += ball_speed_x
            ball_y += ball_speed_y

            # Bounce ball off walls
            if ball_x <= 0 or ball_x >= WINDOW_SIZE[0] - BALL_RADIUS * 2:
                ball_speed_x *= -1

            if ball_y <= 0:
                ball_speed_y *= -1

            # Check collision with paddle
            if ball_y >= paddle_y - BALL_RADIUS and paddle_x < ball_x < paddle_x + PADDLE_WIDTH:
                ball_speed_y *= -1
                paddle_hit_sound.play()

            # Check collision with bricks
            for brick in bricks:
                if brick.colliderect(pygame.Rect(ball_x, ball_y, BALL_RADIUS * 2, BALL_RADIUS * 2)):
                    ball_speed_y *= -1
                    brick_hit_sound.play()
                    bricks.remove(brick)
                    score += 10

            # Check if all bricks are broken
            if len(bricks) == 0:
                current_level += 1
                if current_level < len(levels):
                    bricks = levels[current_level]
                    ball_x = WINDOW_SIZE[0] // 2
                    ball_y = WINDOW_SIZE[1] // 2
                    ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
                    ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])
                else:
                    game_completed()

            # Check if ball falls off the screen
            if ball_y >= WINDOW_SIZE[1]:
                lives -= 1
                if lives > 0:
                    ball_x = WINDOW_SIZE[0] // 2
                    ball_y = WINDOW_SIZE[1] // 2
                    ball_speed_x = BALL_SPEED_X * random.choice([-1, 1])
                    ball_speed_y = BALL_SPEED_Y * random.choice([-1, 1])
                    paused = True
                else:
                    game_over_sound.play()
                    game_over()

            # Move the paddle
            paddle_x += paddle_speed
            if paddle_x < 0:
                paddle_x = 0
            elif paddle_x > WINDOW_SIZE[0] - PADDLE_WIDTH:
                paddle_x = WINDOW_SIZE[0] - PADDLE_WIDTH

        # Clear the screen
        screen.fill(BLACK)

        # Draw ball and paddle
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

        # Draw bricks
        for brick in bricks:
            pygame.draw.rect(screen, WHITE, brick)

        # Draw score and lives
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Lives: {lives}", font, WHITE, 699, 10)
        
        if paused:
            draw_text("Paused", pygame.font.Font(None, 80), WHITE, 300, 250)

        # Update the display
        pygame.display.flip()

        clock.tick(60)

# Game completed function
def game_completed():
    font = pygame.font.Font(None, 80)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Congratulations!", font, WHITE, 150, 250)
        draw_text("Press 'Q' to Quit", font, WHITE, 230, 350)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Game over function
def game_over():
    font = pygame.font.Font(None, 80)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        draw_text("Game Over", font, WHITE, 250, 250)
        draw_text("Press 'R' to Restart", font, WHITE, 200, 350)
        draw_text("Press 'Q' to Quit", font, WHITE, 230, 450)

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            start_game()
        elif keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def game_menu():
    menu_font = pygame.font.Font(None, 50)
    selected_option = "Start Game"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = "Start Game"
                elif event.key == pygame.K_DOWN:
                    selected_option = "Credits"  # Added a new option for viewing credits
                elif event.key == pygame.K_RETURN:
                    if selected_option == "Start Game":
                        start_game()
                    elif selected_option == "Quit":
                        pygame.quit()
                        sys.exit()
                    elif selected_option == "Credits":
                        display_credits()  # Display the credits when "Credits" is selected

        # Draw menu
        screen.fill(BLACK)
        draw_text("Game Menu", menu_font, WHITE, 300, 200)

        if selected_option == "Start Game":
            draw_text("> Start Game", menu_font, RED, 280, 300)
            draw_text("Credits", menu_font, WHITE, 320, 350)  # Display "Credits" as the new option
        elif selected_option == "Credits":
            draw_text("Start Game", menu_font, WHITE, 280, 300)
            draw_text("> Credits", menu_font, RED, 320, 350)  # Highlight "Credits" when selected

        pygame.display.flip()


# Run the menu loop
game_menu()
