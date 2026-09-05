import pygame
import math
import array

# Initialize Pygame and Audio Mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Platformer - Mario Style")
clock = pygame.time.Clock()

# Generate a custom retro chiptune jump sound programmatically
def create_retro_jump_sound():
    sample_rate = 22050
    duration = 0.15  # seconds
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    
    # Frequency sweep up (classic 8-bit jump sound)
    for i in range(n_samples):
        t = float(i) / sample_rate
        freq = 150 + (t / duration) * 450  # Sweep from 150Hz to 600Hz
        # Square wave sound
        val = 16000 if math.sin(2 * math.pi * freq * t) > 0 else -16000
        # Envelope fade out at the end
        fade = 1.0 - (i / n_samples)
        buf.append(int(val * fade))
        
    return pygame.mixer.Sound(buffer=buf)

JUMP_SOUND = create_retro_jump_sound()

# --- GAME CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 40))
        self.image.fill((220, 50, 50))  # Red Mario-style color
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.score = 0

    def update(self, platforms):
        # Gravity
        self.vy += 0.6
        if self.vy > 12:
            self.vy = 12

        # Horizontal Movement
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -4
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = 4

        # Move X & Check Collision
        self.rect.x += self.vx
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vx > 0:
                    self.rect.right = platform.rect.left
                elif self.vx < 0:
                    self.rect.left = platform.rect.right

        # Move Y & Check Collision
        self.rect.y += self.vy
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vy > 0:
                    self.rect.bottom = platform.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.rect.bottom
                    self.vy = 0

    def jump(self):
        if self.on_ground:
            self.vy = -12
            JUMP_SOUND.play()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(100, 200, 100)):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 215, 0))  # Gold
        self.rect = self.image.get_rect(center=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, distance):
        super().__init__()
        self.image = pygame.Surface((28, 28))
        self.image.fill((139, 69, 19))  # Brown Goomba color
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.distance = distance
        self.speed = 1.5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > self.start_x + self.distance or self.rect.x < self.start_x:
            self.speed *= -1

# --- GAME SETUP ---

player = Player(50, 300)
all_sprites = pygame.sprite.Group(player)

platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Level Design
level_data = [
    # Ground
    Platform(0, 400, 1200, 50, (30, 160, 30)),
    # Platforms
    Platform(200, 300, 120, 20),
    Platform(380, 220, 100, 20),
    Platform(550, 320, 140, 20),
    Platform(750, 240, 120, 20),
]

for p in level_data:
    platforms.add(p)
    all_sprites.add(p)

# Add Coins
for pos in [(230, 260), (260, 260), (410, 180), (580, 280), (610, 280)]:
    c = Coin(*pos)
    coins.add(c)
    all_sprites.add(c)

# Add Goomba-style Enemies
e1 = Enemy(220, 372, 100)
e2 = Enemy(560, 292, 80)
enemies.add(e1, e2)
all_sprites.add(e1, e2)

# Camera Offset
camera_x = 0

# --- MAIN LOOP ---
running = True
font = pygame.font.SysFont(None, 32)

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                player.jump()

    # Update
    player.update(platforms)
    enemies.update()

    # Coin Collect
    collected = pygame.sprite.spritecollide(player, coins, True)
    for coin in collected:
        player.score += 10

    # Enemy Collision (Stomp vs Get Hit)
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    for enemy in enemy_hits:
        # Check if player stomped on top of enemy
        if player.vy > 0 and player.rect.bottom <= enemy.rect.top + 12:
            enemy.kill()
            player.vy = -8  # Bounce off enemy
            player.score += 20
        else:
            # Player hit from side - reset position
            player.rect.topleft = (50, 300)

    # Camera Follow Player
    camera_x = player.rect.x - WIDTH // 3

    # Render
    screen.fill((135, 206, 235))  # Sky blue background

    # Render all objects with camera offset
    for sprite in all_sprites:
        offset_rect = sprite.rect.move(-camera_x, 0)
        screen.blit(sprite.image, offset_rect)

    # Draw Score HUD
    score_text = font.render(f"Coins: {player.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()