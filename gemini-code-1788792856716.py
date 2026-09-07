import pygame
import math
import array
import random

# --- INITIALIZATION ---
pygame.init()
# Set up 2 audio channels: 1 for sound effects, 1 for looping music
pygame.mixer.init(frequency=22050, size=-16, channels=2)

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Shift - Cyber Dash")
clock = pygame.time.Clock()

# --- COLOR PALETTE ---
COLOR_CYAN = (0, 255, 240)
COLOR_PINK = (255, 0, 127)
COLOR_DARK = (15, 10, 25)

# --- PROCEDURAL SOUND GENERATOR ---
def synth_sound(freq_start, freq_end, duration, wave_type="sine", fade=True):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    
    for i in range(n_samples):
        t = float(i) / sample_rate
        progress = i / n_samples
        freq = freq_start + (freq_end - freq_start) * progress
        
        if wave_type == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif wave_type == "square":
            val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        elif wave_type == "sawtooth":
            val = 2.0 * (freq * t - math.floor(0.5 + freq * t))
        elif wave_type == "noise":
            val = random.uniform(-1.0, 1.0)
            
        amplitude = 12000
        if fade:
            amplitude *= (1.0 - progress)
            
        buf.append(int(val * amplitude))
        
    return pygame.mixer.Sound(buffer=buf)

# --- SYNTHWAVE MUSIC GENERATOR ---
def generate_synthwave_bgm():
    sample_rate = 22050
    bpm = 120
    beat_duration = 60.0 / bpm  # 0.5s per beat
    step_duration = beat_duration / 2  # 8th notes (0.25s)
    
    # 16-step bassline sequence (A minor baseline)
    bass_freqs = [
        110.0, 110.0, 130.81, 110.0,   # A2, A2, C3, A2
        146.83, 110.0, 130.81, 98.0,    # D3, A2, C3, G2
        110.0, 110.0, 164.81, 146.83,  # A2, A2, E3, D3
        130.81, 110.0, 98.0,   123.47   # C3, A2, G2, B2
    ]
    
    # Arpeggiated melody line layered over the bass
    lead_freqs = [
        220.0, 329.63, 440.0, 329.63,
        261.63, 329.63, 440.0, 392.00,
        220.0, 329.63, 523.25, 440.0,
        392.00, 329.63, 293.66, 246.94
    ]
    
    total_samples = int(sample_rate * step_duration * len(bass_freqs))
    buf = array.array('h')
    
    for i in range(total_samples):
        t = float(i) / sample_rate
        step_idx = int(i / (sample_rate * step_duration)) % len(bass_freqs)
        
        # Bass synth (Sawtooth wave for gritty neon feel)
        f_bass = bass_freqs[step_idx]
        val_bass = 2.0 * (f_bass * t - math.floor(0.5 + f_bass * t))
        
        # Lead synth (Square wave for chiptune melody)
        f_lead = lead_freqs[step_idx]
        val_lead = 0.6 if math.sin(2 * math.pi * f_lead * t) > 0 else -0.6
        
        # Percussive beat layer (Kick pulse on every beat)
        beat_t = (i % int(sample_rate * beat_duration)) / sample_rate
        kick_freq = max(40.0, 150.0 * (1.0 - beat_t * 8))
        val_kick = math.sin(2 * math.pi * kick_freq * beat_t) if beat_t < 0.12 else 0.0
        
        # Blend instruments with balanced volume
        mixed_val = (val_bass * 0.35) + (val_lead * 0.25) + (val_kick * 0.40)
        amplitude = 7000
        
        buf.append(int(mixed_val * amplitude))
        
    music_sound = pygame.mixer.Sound(buffer=buf)
    return music_sound

# Generate Audio Effects
SOUND_SHIFT = synth_sound(300, 800, 0.12, "sine")
SOUND_COLLECT = synth_sound(880, 1760, 0.15, "square")
SOUND_HIT = synth_sound(200, 40, 0.25, "noise")

# Generate and start looping background music on Channel 1
BGM = generate_synthwave_bgm()
music_channel = pygame.mixer.Channel(1)
music_channel.play(BGM, loops=-1)

# --- GAME SPRITES ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color_state = "CYAN"  # "CYAN" or "PINK"
        self.rect = pygame.Rect(100, HEIGHT // 2, 36, 36)
        self.vy = 0
        self.health = 100

    def color(self):
        return COLOR_CYAN if self.color_state == "CYAN" else COLOR_PINK

    def toggle_color(self):
        self.color_state = "PINK" if self.color_state == "CYAN" else "CYAN"
        SOUND_SHIFT.play()

    def update(self):
        keys = pygame.key.get_pressed()
        self.vy = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -6
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = 6

        self.rect.y += self.vy
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

class Gate(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.color_state = random.choice(["CYAN", "PINK"])
        self.rect = pygame.Rect(WIDTH + 20, random.randint(50, HEIGHT - 100), 24, 80)
        self.speed = speed

    def color(self):
        return COLOR_CYAN if self.color_state == "CYAN" else COLOR_PINK

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-4, -1)
        self.vy = random.uniform(-1, 1)
        self.color = color
        self.radius = random.randint(3, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.radius -= 0.15

# --- GAME SETUP ---
player = Player()
gates = pygame.sprite.Group()
particles = []

score = 0
gate_speed = 6
spawn_timer = 0

running = True
font = pygame.font.SysFont("Consolas", 28, bold=True)

# --- MAIN LOOP ---
while running:
    clock.tick(60)
    spawn_timer += 1

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.toggle_color()

    # Update Objects
    player.update()
    gates.update()

    # Spawn Gates
    if spawn_timer > 45:
        gates.add(Gate(gate_speed))
        spawn_timer = 0
        gate_speed += 0.05  # Progressive difficulty

    # Trail Particles
    particles.append(Particle(player.rect.left, player.rect.centery, player.color()))
    for p in particles[:]:
        p.update()
        if p.radius <= 0:
            particles.remove(p)

    # Collision Logic
    hits = pygame.sprite.spritecollide(player, gates, True)
    for gate in hits:
        if gate.color_state == player.color_state:
            score += 50
            SOUND_COLLECT.play()
        else:
            player.health -= 25
            SOUND_HIT.play()
            if player.health <= 0:
                running = False  # Game Over

    # --- DRAWING ---
    screen.fill(COLOR_DARK)

    # Grid Lines Background
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (30, 20, 55), (0, y), (WIDTH, y), 1)

    # Draw Particles
    for p in particles:
        pygame.draw.circle(screen, p.color, (int(p.x), int(p.y)), max(1, int(p.radius)))

    # Draw Gates
    for gate in gates:
        pygame.draw.rect(screen, gate.color(), gate.rect, border_radius=6)

    # Draw Player
    pygame.draw.rect(screen, player.color(), player.rect, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), player.rect, 2, border_radius=8)

    # Draw HUD
    score_txt = font.render(f"SCORE: {score}", True, (255, 255, 255))
    health_txt = font.render(f"HP: {player.health}%", True, COLOR_CYAN if player.health > 50 else COLOR_PINK)
    screen.blit(score_txt, (20, 20))
    screen.blit(health_txt, (WIDTH - 150, 20))

    pygame.display.flip()

pygame.quit()