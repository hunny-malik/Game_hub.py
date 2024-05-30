import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
FONT_SIZE = 48
FPS = 60

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Functions
def draw_grid():
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // 3, 0), (i * WIDTH // 3, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // 3), (WIDTH, i * HEIGHT // 3), LINE_WIDTH)

def draw_x(row, col):
    pygame.draw.line(screen, X_COLOR, (col * WIDTH // 3 + WIDTH // 12, row * HEIGHT // 3 + HEIGHT // 12),
                     ((col + 1) * WIDTH // 3 - WIDTH // 12, (row + 1) * HEIGHT // 3 - HEIGHT // 12), LINE_WIDTH)

    pygame.draw.line(screen, X_COLOR, ((col + 1) * WIDTH // 3 - WIDTH // 12, row * HEIGHT // 3 + HEIGHT // 12),
                     (col * WIDTH // 3 + WIDTH // 12, (row + 1) * HEIGHT // 3 - HEIGHT // 12), LINE_WIDTH)

def draw_o(row, col):
    pygame.draw.circle(screen, O_COLOR, (col * WIDTH // 3 + WIDTH // 6, row * HEIGHT // 3 + HEIGHT // 6),
                       min(WIDTH // 6, HEIGHT // 6) - LINE_WIDTH // 2, LINE_WIDTH)

def draw_winner(result):
    text = font.render(result, True, LINE_COLOR)
    screen.blit(text, (WIDTH // 6, HEIGHT // 2 - FONT_SIZE // 2))

def draw_board(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_x(row, col)
            elif board[row][col] == 'O':
                draw_o(row, col)

def check_winner(board):
    # Check rows, columns, and diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ' or \
            board[0][i] == board[1][i] == board[2][i] != ' ':
            return True

    if board[0][0] == board[1][1] == board[2][2] != ' ' or \
        board[0][2] == board[1][1] == board[2][0] != ' ':
        return True

    return False

def check_tie(board):
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def computer_move(board):
    # Check for a winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ' and is_winning_move(board, i, j, 'O'):
                return i, j

    # Check for a blocking move
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ' and is_winning_move(board, i, j, 'X'):
                return i, j

    # Choose a random move if no strategic move found
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    if available_moves:
        return random.choice(available_moves)
    return None

def is_winning_move(board, row, col, player):
    temp_board = [row[:] for row in board]  # Create a copy of the board
    temp_board[row][col] = player
    return check_winner(temp_board)

# Game loop
def game():
    # Initialize the board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    human_player = 'X'
    computer_player = 'O'
    current_player = human_player
    game_over = False
    winner = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over and current_player == human_player:
                x, y = pygame.mouse.get_pos()
                col = x // (WIDTH // 3)
                row = y // (HEIGHT // 3)
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    if check_winner(board):
                        winner = "Human player wins!"
                        game_over = True
                    elif check_tie(board):
                        winner = "It's a tie!"
                        game_over = True
                    else:
                        current_player = computer_player

        # Computer's turn
        if current_player == computer_player and not game_over:
            move = computer_move(board)
            if move:
                row, col = move
                board[row][col] = 'O'
                if check_winner(board):
                    winner = "Computer wins!"
                    game_over = True
                elif check_tie(board):
                    winner = "It's a tie!"
                    game_over = True
                else:
                    current_player = human_player

        # Draw everything
        screen.fill(WHITE)
        draw_grid()
        draw_board(board)
        if winner:
            draw_winner(winner)
            pygame.display.flip()
            pygame.time.wait(2000)  # Display result for 2 seconds
            return

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

def main():
    while True:
        game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
