import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load assets (placeholders for now)
# Replace with actual file paths
BACKGROUND_IMAGE = "background.png"
SPACESHIP_IMAGE = "spaceship.png"
ASTEROID_IMAGE = "asteroid.png"
CRYSTAL_IMAGE = "energy_crystal.png"
BACKGROUND_MUSIC = "background_music.wav"
COLLECT_SOUND = "clash_sound.wav"


# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Load images
background = pygame.image.load(BACKGROUND_IMAGE)
spaceship = pygame.image.load(SPACESHIP_IMAGE)
asteroid_img = pygame.image.load(ASTEROID_IMAGE)
energy_crystal_img = pygame.image.load(CRYSTAL_IMAGE)

# Scale images
spaceship = pygame.transform.scale(spaceship, (50, 50))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))
energy_crystal_img = pygame.transform.scale(energy_crystal_img, (30, 30))

# Load sounds
pygame.mixer.music.load(BACKGROUND_MUSIC)
collect_sound = pygame.mixer.Sound(COLLECT_SOUND)

# Start background music
pygame.mixer.music.play(-1)

# Game clock
clock = pygame.time.Clock()

# Game variables
spaceship_x, spaceship_y = WIDTH // 2, HEIGHT - 70
spaceship_speed = 5

asteroids = []
crystals = []

score = 0
lives = 3

difficulty_timer = 0
asteroid_speed = 3
asteroid_size = 50

# Font
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def spawn_asteroid():
    x = random.randint(0, WIDTH - asteroid_size)
    asteroids.append({"x": x, "y": -asteroid_size})

def spawn_crystal():
    x = random.randint(0, WIDTH - 30)
    crystals.append({"x": x, "y": -30})

# Game loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < WIDTH - 50:
        spaceship_x += spaceship_speed

    # Update asteroids
    for asteroid in asteroids[:]:
        asteroid["y"] += asteroid_speed
        if asteroid["y"] > HEIGHT:
            asteroids.remove(asteroid)

        # Collision check
        if (
            spaceship_x < asteroid["x"] + asteroid_size and
            spaceship_x + 50 > asteroid["x"] and
            spaceship_y < asteroid["y"] + asteroid_size and
            spaceship_y + 50 > asteroid["y"]
        ):
            lives -= 1
            asteroids.remove(asteroid)
            if lives == 0:
                draw_text("Game Over", WIDTH // 2 - 100, HEIGHT // 2, RED)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

    # Update crystals
    for crystal in crystals[:]:
        crystal["y"] += 2
        if crystal["y"] > HEIGHT:
            crystals.remove(crystal)

        # Collection check
        if (
            spaceship_x < crystal["x"] + 30 and
            spaceship_x + 50 > crystal["x"] and
            spaceship_y < crystal["y"] + 30 and
            spaceship_y + 50 > crystal["y"]
        ):
            score += 10
            collect_sound.play()
            crystals.remove(crystal)

    # Check for successful completion
    if score >= 350:
        draw_text("You Win!", WIDTH // 2 - 100, HEIGHT // 2, GREEN)
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    # Increase difficulty based on score
    if score >= 200:
        asteroid_size = 70
        asteroid_img = pygame.transform.scale(pygame.image.load(ASTEROID_IMAGE), (asteroid_size, asteroid_size))
        spaceship_speed = 7

    # Draw spaceship
    screen.blit(spaceship, (spaceship_x, spaceship_y))

    # Draw asteroids
    for asteroid in asteroids:
        screen.blit(asteroid_img, (asteroid["x"], asteroid["y"]))

    # Draw crystals
    for crystal in crystals:
        screen.blit(energy_crystal_img, (crystal["x"], crystal["y"]))

    # Spawn new objects
    if random.randint(1, 30) == 1:
        spawn_asteroid()
    if random.randint(1, 50) == 1:
        spawn_crystal()

    # Difficulty increase
    difficulty_timer += 1
    if difficulty_timer % 500 == 0:
        asteroid_speed += 1

    # Draw HUD
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {lives}", 10, 50)

    # Update screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
