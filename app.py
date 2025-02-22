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
WIDTH, HEIGHT = 600, 600
FPS = 60
GRAVITY = 0.5 # default is 0.5 this determines the height of a flap and fall speed
FLAP_STRENGTH = -10 # default is -10 this combined with gravity determines the height of a flap
PIPE_WIDTH = 40 # default is 60
PIPE_GAP = 200 # default is 150
PIPE_SPEED = 3 # default is 3
PIPE_FREQUENCY = 1500  # milliseconds between new pipes
GAME_CHARACTER = "Pam"  # Options: "Koala", "Pam"
GAME_TITLE = (
    "Flappy Koala 🐨 by Manu Codes" 
    if GAME_CHARACTER == "Koala" 
    else "Flappy Pam 🐦 by Manu Codes"
)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BROWN = (139, 69, 19)

# Character-specific settings
CHARACTER_COLORS = {
    "Koala": BROWN,
    "Pam": (255, 192, 203)  # Pink for Pam
}

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Load available assets
for img_name in ['koala.png', 'pam.png', 'pipe.png', 'background.png']:
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
class Character:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.radius = 20
        self.velocity = 0
        # Try to load character-specific image
        self.image = IMAGES.get(GAME_CHARACTER.lower())
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
            # Fallback to circle with character-specific color
            color = CHARACTER_COLORS.get(GAME_CHARACTER, BROWN)  # Default to brown if character not found
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)

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

def reset_game():
    """Reset game state for a new game"""
    character = Character()
    pipes = []
    score = 0
    return character, pipes, score

def main():
    koala, pipes, score = reset_game()
    font = pygame.font.SysFont("Arial", 32)
    game_active = True
    
    # Set up a timer event to spawn pipes periodically
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
                    if game_active:
                        koala.flap()
                    else:
                        # Reset game on spacebar when game is over
                        koala, pipes, score = reset_game()
                        game_active = True
            if event.type == SPAWNPIPE and game_active:
                pipes.append(Pipe())

        if game_active:
            # Update game objects
            koala.update()
            for pipe in pipes:
                pipe.update()

            # Increase score when koala passes a pipe
            for pipe in pipes:
                if pipe.x + pipe.width < koala.x and not hasattr(pipe, 'scored'):
                    score += 1
                    pipe.scored = True
                    if SOUNDS.get('score'):
                        SOUNDS['score'].play()

            # Remove off-screen pipes
            pipes = [pipe for pipe in pipes if not pipe.off_screen()]

            # Check for collisions
            if check_collision(koala, pipes):
                game_active = False
                if SOUNDS.get('hit'):
                    SOUNDS['hit'].play()

        # Draw everything
        screen.fill(WHITE)
        koala.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw game over message
        if not game_active:
            game_over_text = font.render("Game Over! Press SPACE to restart", True, BLACK)
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()