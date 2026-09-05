import pygame
import random
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Physics Particle Fountain")
clock = pygame.time.Clock()

# Particle class handling physics and rendering
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.uniform(3, 8)
        
        # Velocity with slight random variation
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Physics parameters
        self.gravity = 0.25
        self.bounce = 0.75
        self.friction = 0.99
        
        # Appearance
        self.color = [random.randint(50, 255), random.randint(100, 255), random.randint(200, 255)]
        self.life = 255  # Opacity / Lifespan
        self.decay = random.uniform(0.8, 2.0)

    def update(self):
        # Apply physics
        self.vy += self.gravity
        self.vx *= self.friction
        self.vy *= self.friction
        
        self.x += self.vx
        self.y += self.vy

        # Bounce off screen boundaries
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -self.bounce
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -self.bounce

        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -self.bounce

        # Reduce lifespan
        self.life -= self.decay

    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, int(self.life))
            
            # Create a glowing effect using a separate surface with per-pixel alpha
            s = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            
            # Inner circle
            pygame.draw.circle(s, color_with_alpha, (self.radius * 2, self.radius * 2), self.radius)
            # Outer glow
            pygame.draw.circle(s, (*self.color, alpha // 3), (self.radius * 2, self.radius * 2), self.radius * 2)
            
            surface.blit(s, (self.x - self.radius * 2, self.y - self.radius * 2))

# Main loop
particles = []
running = True

while running:
    clock.tick(60)
    screen.fill((10, 10, 18))  # Dark background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn particles at mouse location when clicked or moved
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:  # Left click pressed
        mx, my = pygame.mouse.get_pos()
        for _ in range(8):
            particles.append(Particle(mx, my))

    # Update and render particles
    for p in particles[:]:
        p.update()
        p.draw(screen)
        if p.life <= 0:
            particles.remove(p)

    # Display particle count
    font = pygame.font.SysFont(None, 24)
    img = font.render(f"Particles: {len(particles)} (Click and drag mouse)", True, (200, 200, 200))
    screen.blit(img, (10, 10))

    pygame.display.flip()

pygame.quit()