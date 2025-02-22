import sys
import random
import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 60
PIPE_GAP = 150
PIPE_SPEED = 3
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

# Koala class: represents our flying koala
class Koala:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.radius = 20  # used for drawing as a circle
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, surface):
        # Draw a circle to represent the koala.
        # Replace this with an image if desired.
        pygame.draw.circle(surface, BROWN, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        # Return a rect that approximates the koala's bounds.
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Pipe class: represents each obstacle pair
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.width = PIPE_WIDTH
        # Randomize the gap position, keeping margins
        self.top_height = random.randint(50, HEIGHT - PIPE_GAP - 50)
        self.bottom_y = self.top_height + PIPE_GAP

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, surface):
        # Draw top pipe
        pygame.draw.rect(surface, GREEN, (self.x, 0, self.width, self.top_height))
        # Draw bottom pipe
        pygame.draw.rect(surface, GREEN, (self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y))

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