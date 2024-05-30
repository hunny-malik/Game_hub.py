import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 30
GRAVITY = 1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (0, 200, 0)

# Player variables
player_size = 30
player_x = WIDTH // 4
player_y = HEIGHT // 2
player_velocity = 0
gravity = GRAVITY
jump_strength = -12

# Pipe variables
pipe_width = 50
pipe_height = random.randint(100, 300)
pipe_x = WIDTH
pipe_gap = 150
pipe_speed = 5

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Function to display the score
def show_score(score):
    score_display = font.render("Score: " + str(score), True, BLACK)
    screen.blit(score_display, (10, 10))

# Function to display a message
def display_message(message, y_offset=0):
    message_display = font.render(message, True, BLACK)
    screen.blit(message_display, (WIDTH // 2 - message_display.get_width() // 2, HEIGHT // 2 + y_offset))

# Function to draw the retry button
def draw_retry_button():
    pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 40))
    retry_text = font.render("Retry", True, BLACK)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 70))

# Main game loop
game_active = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                player_velocity = jump_strength
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_active:
            # Check if the mouse click is within the retry button area
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if WIDTH // 2 - 50 <= mouse_x <= WIDTH // 2 + 50 and HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 90:
                # Reset game variables
                player_y = HEIGHT // 2
                player_velocity = 0
                pipe_x = WIDTH
                pipe_height = random.randint(100, 300)
                score = 0
                game_active = True

    if game_active:
        # Update player position
        player_velocity += gravity
        player_y += player_velocity

        # Update pipe position
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = WIDTH
            pipe_height = random.randint(100, 300)
            score += 1
            if score % 5 == 0:
                pipe_gap -= 5 

        # Check for collisions with pipes
        if (
            player_x < pipe_x + pipe_width
            and player_x + player_size > pipe_x
            and (player_y < pipe_height or player_y + player_size > pipe_height + pipe_gap)
        ):
            game_active = False

        # Check if the player is out of the screen
        if player_y < 0 or player_y + player_size > HEIGHT:
            game_active = False

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (player_x, player_y, player_size, player_size))
        pygame.draw.rect(screen, RED, (pipe_x, 0, pipe_width, pipe_height))
        pygame.draw.rect(
            screen,
            RED,
            (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap),
        )

        # Display the score
        show_score(score)
    else:
        # Display game over message
        display_message("Game Over", y_offset=-50)
        display_message("Your score: " + str(score), y_offset=0)
        pipe_gap = 150
        draw_retry_button()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
