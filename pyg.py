import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bird Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
GOLD = (255, 215, 0)

# Game variables
levels = [
    {'level': 1, 'health': 5, 'time': 30, 'birds': 7},
    {'level': 2, 'health': 7, 'time': 30, 'birds': 12},
    {'level': 3, 'health': 9, 'time': 30, 'birds': 17},
    {'level': 4, 'health': 11, 'time': 30, 'birds': 22},
    {'level': 5, 'health': 13, 'time': 40, 'birds': 27},
    {'level': 6, 'health': 15, 'time': 40, 'birds': 32},
    {'level': 7, 'health': 17, 'time': 40, 'birds': 37},
    {'level': 8, 'health': 19, 'time': 40, 'birds': 42},
    {'level': 9, 'health': 21, 'time': 40, 'birds': 50},
    {'level': 10, 'health': 23, 'time': 40, 'birds': 55},
]

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self, color, value):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 20)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 20)
        self.value = value

# Initialize variables
clock = pygame.time.Clock()
running = True
current_level = 0
score = 0
bird_group = pygame.sprite.Group()

# Function to start a level
def start_level(level):
    global bird_group
    bird_group.empty()
    level_data = levels[level]
    for _ in range(level_data['birds']):
        bird_type = random.choice(['normal', 'silver', 'gold'])
        if bird_type == 'normal':
            bird = Bird(BLACK, 1)
        elif bird_type == 'silver' and level_data['level'] in [3, 5]:
            bird = Bird(SILVER, 1.2)
        elif bird_type == 'gold' and level_data['level'] in [4, 6]:
            bird = Bird(GOLD, 2)
        else:
            bird = Bird(BLACK, 1)
        bird_group.add(bird)

# Start the first level
start_level(current_level)

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    screen.fill(WHITE)
    
    # Draw birds
    bird_group.draw(screen)
    
    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()