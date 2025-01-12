import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 650
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TIMER_BAR_COLOR = (0, 200, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

board = [[None for _ in range(COLS)] for _ in range(ROWS)]

pygame.font.init()
font = pygame.font.SysFont("Arial", 40)

GAME_TIME = 30
start_ticks = pygame.time.get_ticks()

confetti_particles = []

class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(5, 10)
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.size = max(0, self.size - 0.1)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), int(self.size))

def draw_board():
    board_top = SQUARE_SIZE // 2
    for row in range(ROWS):
        for col in range(COLS):
            color = board[row][col] if board[row][col] else GRAY
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, board_top + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, board_top + row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

def draw_timer_bar(time_left):
    bar_width = int((time_left / GAME_TIME) * WIDTH)
    pygame.draw.rect(screen, TIMER_BAR_COLOR, (0, 0, bar_width, SQUARE_SIZE // 2))
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE // 2), 2)

    timer_text = font.render(f"Време: {max(0, time_left)} сек.", True, BLACK)
    text_rect = timer_text.get_rect(center=(WIDTH // 2, SQUARE_SIZE // 4))
    screen.blit(timer_text, text_rect)

def get_neighbors(row, col):
    neighbors = []
    if row > 0: neighbors.append((row - 1, col))
    if row < ROWS - 1: neighbors.append((row + 1, col))
    if col > 0: neighbors.append((row, col - 1))
    if col < COLS - 1: neighbors.append((row, col + 1))
    return neighbors

def is_valid_move(row, col, color):
    for neighbor in get_neighbors(row, col):
        n_row, n_col = neighbor
        if board[n_row][n_col] == color:
            return False
    return True

def check_win():
    for row in board:
        if None in row:
            return False
    return True

def display_message(message, size=40):
    pygame.draw.rect(screen, WHITE, (100, HEIGHT // 2 - 50, WIDTH - 200, 100))
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_sad_faces():
    sad_face = pygame.font.SysFont("Arial", 30).render("Времето истече!:(", True, (255, 0, 0))
    screen.blit(sad_face, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

def main():
    selected_color = COLORS[0]
    running = True
    game_won = False
    game_over = False

    while running:
        screen.fill(WHITE)

        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = GAME_TIME - seconds_passed

        if time_left <= 0 and not game_won:
            game_over = True

        draw_timer_bar(time_left)

        if not game_over and not game_won:
            draw_board()
        elif game_over:
            draw_sad_faces()
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False
        elif game_won:
            if len(confetti_particles) == 0:
                for _ in range(200):
                    confetti_particles.append(Confetti())

            for confetti in confetti_particles:
                confetti.move()
                confetti.draw()

            display_message("Честитки! Победивте!")
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_won and not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    row, col = (y - SQUARE_SIZE // 2) // SQUARE_SIZE, x // SQUARE_SIZE

                    if 0 <= row < ROWS and 0 <= col < COLS:
                        if board[row][col] is None and is_valid_move(row, col, selected_color):
                            board[row][col] = selected_color

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        selected_color = COLORS[0]
                    elif event.key == pygame.K_2:
                        selected_color = COLORS[1]
                    elif event.key == pygame.K_3:
                        selected_color = COLORS[2]
                    elif event.key == pygame.K_4:
                        selected_color = COLORS[3]

        if check_win() and not game_won:
            game_won = True

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
