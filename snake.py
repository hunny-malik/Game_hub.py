import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 600, 400
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Nokia Snake Game")

# Set up colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Set up the snake
snake_size = 20
snake_speed = 8  # Adjusted for a slower speed
snake = [(width // 2, height // 2)]
snake_direction = (1, 0)

# Set up the food
food_size = 20
food = (random.randrange(0, width - food_size, food_size),
        random.randrange(0, height - food_size, food_size))

# Set up the score
score = 0
font = pygame.font.Font(None, 36)

# Set up the clock
clock = pygame.time.Clock()

# Function to reset the game state
def reset_game():
    global snake, snake_direction, food, score
    snake = [(width // 2, height // 2)]
    snake_direction = (1, 0)
    food = (random.randrange(0, width - food_size, food_size),
            random.randrange(0, height - food_size, food_size))
    score = 0

# Function to display retry button
def draw_retry_button():
    pygame.draw.rect(window, white, (width // 4, height // 2, width // 2, 50))
    retry_text = font.render("Retry", True, black)
    window.blit(retry_text, (width // 2 - retry_text.get_width() // 2, height // 2 + 10))

# Main game loop
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game_over:
            reset_game()
            game_over = False
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if width // 4 <= mouse_x <= width // 4 + width // 2 and height // 2 <= mouse_y <= height // 2 + 50:
                reset_game()
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_direction != (0, 1):
            snake_direction = (0, -1)
        elif keys[pygame.K_DOWN] and snake_direction != (0, -1):
            snake_direction = (0, 1)
        elif keys[pygame.K_LEFT] and snake_direction != (1, 0):
            snake_direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and snake_direction != (-1, 0):
            snake_direction = (1, 0)

        # Move the snake
        x, y = snake[0]
        x += snake_direction[0] * snake_size
        y += snake_direction[1] * snake_size
        snake.insert(0, (x, y))

        # Check if the snake touches the side of the window
        if x < 0 or x >= width or y < 0 or y >= height:
            game_over = True

        # Check if the snake eats the food
        if x == food[0] and y == food[1]:
            food = (random.randrange(0, width - food_size, food_size),
                    random.randrange(0, height - food_size, food_size))
            score += 1
        else:
            # If not, remove the last segment of the snake
            snake.pop()

    # Draw everything
    window.fill(white)

    if game_over:
        draw_retry_button()
    else:
        pygame.draw.rect(window, red, (food[0], food[1], food_size, food_size))
        for segment in snake:
            pygame.draw.rect(window, black, (segment[0], segment[1], snake_size, snake_size))

    # Draw the score
    score_text = font.render(f"Score: {score}", True, black)
    window.blit(score_text, (10, 10))

    pygame.display.flip()

    # Control the snake speed
    clock.tick(snake_speed)
