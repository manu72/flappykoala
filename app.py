import sys
import random
import os
import pygame

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound

# Asset loading
ASSET_DIR = os.path.join(os.path.dirname(__file__), 'assets')
IMAGES = {}
SOUNDS = {}

def load_image(name):
    path = os.path.join(ASSET_DIR, 'images', name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error:
        return None

def load_sound(name):
    path = os.path.join(ASSET_DIR, 'sounds', name)
    if not os.path.exists(path):
        return None
    try:
        return pygame.mixer.Sound(path)
    except pygame.error:
        return None

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5 # default is 0.5 this determines the height of a flap and fall speed
FLAP_STRENGTH = -10 # default is -10 this combined with gravity determines the height of a flap
PIPE_WIDTH = 60 # default is 60
PIPE_GAP = 200 # default is 150
PIPE_SPEED = 3 # default is 3
PIPE_FREQUENCY = 1500  # milliseconds between new pipes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Koala")
clock = pygame.time.Clock()

# Load available assets
for img_name in ['koala.png', 'pipe.png', 'background.png']:
    if img := load_image(img_name):
        IMAGES[img_name.split('.')[0]] = img

for sound_name in ['flap.wav', 'score.wav', 'hit.wav']:
    if snd := load_sound(sound_name):
        SOUNDS[sound_name.split('.')[0]] = snd

# Debug print available images
print("\nAvailable images:")
for name in IMAGES:
    print(f"- {name}")

# Koala class: represents our flying koala
class Koala:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.radius = 20
        self.velocity = 0
        self.image = IMAGES.get('koala')
        if self.image:
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def flap(self):
        self.velocity = FLAP_STRENGTH
        if SOUNDS.get('flap'):
            SOUNDS['flap'].play()

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        if self.image:
            self.rect.center = (self.x, self.y)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, self.rect)
        else:
            # Fallback to circle
            pygame.draw.circle(surface, BROWN, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        if self.image:
            return self.rect
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                         self.radius * 2, self.radius * 2)

# Pipe class: represents each obstacle pair
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = PIPE_WIDTH
        self.top_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.bottom_y = self.top_height + PIPE_GAP
        self.image = IMAGES.get('pipe')
    
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, surface):
        if self.image:
            # Draw top pipe (flipped)
            top_pipe = pygame.transform.flip(self.image, False, True)
            surface.blit(top_pipe, (self.x, self.top_height - self.image.get_height()))
            # Draw bottom pipe
            surface.blit(self.image, (self.x, self.bottom_y))
        else:
            # Fallback to rectangles
            pygame.draw.rect(surface, GREEN, (self.x, 0, self.width, self.top_height))
            pygame.draw.rect(surface, GREEN, (self.x, self.bottom_y, self.width, 
                           HEIGHT - self.bottom_y))

    def off_screen(self):
        return self.x < -self.width

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.top_height)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y)

# Function to check for collisions between the koala and pipes or boundaries.
def check_collision(koala, pipes):
    koala_rect = koala.get_rect()

    # Check collision with the top and bottom of the screen.
    if koala.y - koala.radius < 0 or koala.y + koala.radius > HEIGHT:
        return True

    # Check collision with each pipe.
    for pipe in pipes:
        if koala_rect.colliderect(pipe.get_top_rect()) or koala_rect.colliderect(pipe.get_bottom_rect()):
            return True
    return False

# Main game loop
def main():
    score = 0
    font = pygame.font.SysFont("Arial", 32)
    koala = Koala()
    pipes = []
    
    # Set up a timer event to spawn pipes periodically.
    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, PIPE_FREQUENCY)

    running = True
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    koala.flap()
            if event.type == SPAWNPIPE:
                pipes.append(Pipe())

        # Update game objects
        koala.update()
        for pipe in pipes:
            pipe.update()

        # Increase score when the koala passes a pipe (only once per pipe)
        for pipe in pipes:
            if pipe.x + pipe.width < koala.x and not hasattr(pipe, 'scored'):
                score += 1
                pipe.scored = True  # mark as scored

        # Remove pipes that have moved off the screen
        pipes = [pipe for pipe in pipes if not pipe.off_screen()]

        # Check for collisions
        if check_collision(koala, pipes):
            running = False

        # Draw everything
        screen.fill(WHITE)
        koala.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    # Game Over: display a message before closing
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2,
                                 (HEIGHT - game_over_text.get_height()) // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()