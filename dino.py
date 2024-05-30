import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 300
GROUND_HEIGHT = 20
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

# Load images
dino_image = pygame.image.load("dino.png")  # Replace with the path to your dino image
cactus_image = pygame.image.load("cactus.png")  # Replace with the path to your cactus image

# Resize images
dino_image = pygame.transform.scale(dino_image, (50, 50))
cactus_image = pygame.transform.scale(cactus_image, (50, 50))

# Game variables
dino_x = 50
dino_y = HEIGHT - GROUND_HEIGHT - 50
dino_speed = 0
jumping = False

cactus_x = WIDTH
cactus_y = HEIGHT - GROUND_HEIGHT - 50
cactus_speed = 5

score = 0

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

class Button:
    def __init__(self, x, y, width, height, color, text, font_size, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font_size = font_size
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

retry_button = Button(WIDTH // 2 - 75, HEIGHT // 2, 150, 50, BLACK, "Retry", 30)

def display_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 40))

# Game loop
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not jumping:
            jumping = True
            dino_speed = -17  # Increase the jump strength

        # Update dino position
        dino_speed += 1  
        dino_y += dino_speed

        if dino_y > HEIGHT - GROUND_HEIGHT - 50:
            dino_y = HEIGHT - GROUND_HEIGHT - 50
            jumping = False

        # Update cactus position
        cactus_x -= cactus_speed
        if cactus_x < 0:
            cactus_x = WIDTH
            cactus_y = HEIGHT - GROUND_HEIGHT - 50
            score += 1

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, 50, 50)
        cactus_rect = pygame.Rect(cactus_x, cactus_y, 50, 50)

        if dino_rect.colliderect(cactus_rect):
            game_over = True

    screen.fill(WHITE)

    if not game_over:
        # Draw everything during the game
        screen.blit(dino_image, (dino_x, dino_y))
        screen.blit(cactus_image, (cactus_x, cactus_y))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        display_score(score)

    else:
        # Draw game over screen
        display_game_over()
        display_score(score)
        retry_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.rect.collidepoint(event.pos):
                    # Reset the game
                    dino_y = HEIGHT - GROUND_HEIGHT - 50
                    cactus_x = WIDTH
                    score = 0
                    jumping = False
                    game_over = False

    pygame.display.flip()
    clock.tick(FPS)
