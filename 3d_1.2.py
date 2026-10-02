from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
import wave
import struct
import os

# --- Sound Synthesis ---
# (Kept identical to previous version for instant execution)
def create_sound_assets():
    sample_rate = 44100

    def write_wav(filename, samples):
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            raw_data = struct.pack('<' + ('h' * len(samples)), *samples)
            wav_file.writeframes(raw_data)

    if not os.path.exists('coin.wav'):
        duration = 0.25
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 987.77 if t < 0.1 else 1318.51
            amplitude = int(18000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('coin.wav', samples)

    if not os.path.exists('jump.wav'):
        duration = 0.2
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 180 + (t / duration) * 320
            amplitude = int(15000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('jump.wav', samples)

    if not os.path.exists('bgm.wav'):
        duration = 4.0
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            wave1 = math.sin(2 * math.pi * 130.81 * t)
            wave2 = 0.5 * math.sin(2 * math.pi * 196.00 * t)
            wave3 = 0.25 * math.sin(2 * math.pi * 261.63 * t)
            combined = (wave1 + wave2 + wave3) / 1.75
            val = int(7000 * combined)
            samples.append(max(min(val, 32767), -32768))
        write_wav('bgm.wav', samples)

create_sound_assets()

# --- Engine & Visual Settings ---
app = Ursina()

window.title = "3D Ruins - Guardian Edition"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# Atmosphere: Sky dome and depth fog
Sky(color=color.hex('#87CEEB'))
scene.fog_density = 0.02
scene.fog_color = color.hex('#a3c2c2')

# Lighting setup
sun = DirectionalLight(y=20, z=-10, shadows=True, rotation=(45, -30, 0))
sun.color = color.rgba(255, 250, 230, 255)
AmbientLight(color=color.rgba(90, 100, 110, 200))

# Audio Instances
bgm = Audio('bgm.wav', loop=True, autoplay=True, volume=0.35)
coin_sfx = Audio('coin.wav', autoplay=False, loop=False, volume=0.7)
jump_sfx = Audio('jump.wav', autoplay=False, loop=False, volume=0.6)

# Ground: Textured check-patterned terrain
ground = Entity(
    model='plane',
    scale=(100, 1, 100),
    color=color.hex('#3b6b35'),
    texture='grass',
    texture_scale=(50, 50),
    collider='box'
)

# --- NEW: Character Model (Procedural Humanoid) ---
class Guardian(Entity):
    def __init__(self, position=(0, 0, 0), rotation_y=0):
        super().__init__(position=position, rotation_y=rotation_y)
        
        # Color palette for the guardian (stone/bronze armor theme)
        armor_col = color.hex('#a89f8c')
        skin_col = color.hex('#c2b280')
        accent_col = color.hex('#5e5443')

        # Torso
        Entity(parent=self, model='cube', scale=(0.8, 1.2, 0.5), y=1.6, color=armor_col, collider='box')
        
        # Head
        Entity(parent=self, model='sphere', scale=0.5, y=2.4, color=skin_col)
        # Helmet Lintel
        Entity(parent=self, model='cube', scale=(0.6, 0.1, 0.6), y=2.6, color=accent_col)

        # Legs
        Entity(parent=self, model='cylinder', scale=(0.25, 1.0, 0.25), position=(-0.25, 0.5, 0), color=accent_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.25, 1.0, 0.25), position=(0.25, 0.5, 0), color=accent_col, collider='box')

        # Arms
        Entity(parent=self, model='cylinder', scale=(0.2, 1.1, 0.2), position=(-0.55, 1.6, 0), rotation_z=15, color=armor_col)
        Entity(parent=self, model='cylinder', scale=(0.2, 1.1, 0.2), position=(0.55, 1.6, 0), rotation_z=-15, color=armor_col)

# --- Environment Procedural 3D Compound Models ---
class Tree(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        # Trunk
        Entity(parent=self, model='cylinder', color=color.hex('#5A3825'), scale=(0.8, 3.5, 0.8), y=1.75, collider='box')
        # Foliage cones
        foliage_layers = [(0, 3.0, 3.8, color.hex('#1d4722')), (0, 4.2, 3.0, color.hex('#265c2c')), (0, 5.4, 2.2, color.hex('#32783a'))]
        for ox, oy, scale_val, col in foliage_layers:
            Entity(parent=self, model='cone', color=col, scale=(scale_val, 2.4, scale_val), y=oy)

class AncientRuin(Entity):
    def __init__(self, position=(0, 0, 0), rotation_y=0):
        super().__init__(position=position, rotation_y=rotation_y)
        stone_col = color.hex('#6e7271')
        moss_col = color.hex('#52574e')
        # Base/Columns/Arch
        Entity(parent=self, model='cube', scale=(4, 0.8, 2), y=0.4, color=moss_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.7, 4, 0.7), position=(-1.3, 2.4, 0), color=stone_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.7, 4, 0.7), position=(1.3, 2.4, 0), color=stone_col, collider='box')
        Entity(parent=self, model='cube', scale=(4.2, 0.8, 1.4), y=4.8, color=stone_col, collider='box')

class Altar(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        Entity(parent=self, model='cylinder', scale=(2.2, 0.4, 2.2), y=0.2, color=color.hex('#474747'), collider='box')
        Entity(parent=self, model='cylinder', scale=(1.4, 0.8, 1.4), y=0.8, color=color.hex('#5c5c5c'), collider='box')

# Populate Environment
# Add Trees
for _ in range(35):
    tx = random.uniform(-42, 42)
    tz = random.uniform(-42, 42)
    if distance((tx, 0, tz), (0, 0, 0)) > 6: Tree(position=(tx, 0, tz))

# Add Ruins
for _ in range(8):
    rx = random.uniform(-38, 38)
    rz = random.uniform(-38, 38)
    if distance((rx, 0, rz), (0, 0, 0)) > 8: AncientRuin(position=(rx, 0, rz), rotation_y=random.randint(0, 360))

# --- NEW: Spawn Guardians near Ruins ---
for _ in range(6):
    gx = random.uniform(-35, 35)
    gz = random.uniform(-35, 35)
    # Ensure they aren't spawning right on top of the player's start position
    if distance((gx, 0, gz), (0, 0, 0)) > 10:
        Guardian(position=(gx, 0, gz), rotation_y=random.randint(0, 360))

# Outer Boundary Stone Wall
wall_dist = 48
wall_height = 5
wall_col = color.hex('#3e4242')
walls = [
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, -wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(wall_dist, wall_height / 2, 0), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(-wall_dist, wall_height / 2, 0), color=wall_col, collider='box')
]

# --- Player Controller ---
player = FirstPersonController(
    speed=9,
    jump_height=1.6,
    origin_y=-0.5,
    position=(0, 2, 0)
)
player.cursor.color = color.rgba(255, 255, 255, 180)

# --- UI Overlay ---
score = 0
score_panel = Entity(parent=camera.ui, model='quad', scale=(0.32, 0.08), position=(-0.68, 0.43), color=color.rgba(0, 0, 0, 140))
score_text = Text(parent=camera.ui, text=f'Gems: {score}', position=(-0.82, 0.45), scale=1.4, color=color.gold)

# --- Collectibles & VFX Particles ---
active_coins = []
active_particles = []

def spawn_coin():
    x = random.uniform(-40, 40)
    z = random.uniform(-40, 40)
    Altar(position=(x, 0, z))
    # Gem model
    coin_root = Entity(position=(x, 1.8, z), base_y=1.8, seed=random.uniform(0, 100))
    Entity(parent=coin_root, model='diamond', scale=(0.9, 1.3, 0.9), color=color.hex('#FFD700'))
    Entity(parent=coin_root, model='sphere', scale=0.4, color=color.white)  # Shiny interior core
    active_coins.append(coin_root)

def trigger_pickup_particles(pos):
    for _ in range(12):
        p = Entity(model='cube', scale=0.12, color=random.choice([color.yellow, color.gold, color.white]), position=pos + Vec3(random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)))
        p.velocity = Vec3(random.uniform(-3, 3), random.uniform(2, 6), random.uniform(-3, 3))
        p.lifetime = 0.5
        active_particles.append(p)

for _ in range(12):
    spawn_coin()

# --- Main Game Loop ---
def update():
    global score
    # Gem animations
    for coin in list(active_coins):
        coin.rotation_y += 90 * time.dt
        coin.y = coin.base_y + math.sin(time.time() * 3 + coin.seed) * 0.25
        # Proximity pickup check
        if distance(player.position, coin.position) < 1.7:
            coin_sfx.play()
            trigger_pickup_particles(coin.position)
            active_coins.remove(coin)
            destroy(coin)
            score += 1
            score_text.text = f'Gems: {score}'
            spawn_coin()

    # Particle physics
    for p in list(active_particles):
        p.position += p.velocity * time.dt
        p.velocity.y -= 12 * time.dt  # Gravity
        p.scale *= 0.94               # Shrink
        p.lifetime -= time.dt
        if p.lifetime <= 0:
            active_particles.remove(p)
            destroy(p)

    # Fall-out reset
    if player.y < -15:
        player.position = (0, 3, 0)

def input(key):
    if key == 'space' and player.grounded: jump_sfx.play()
    if key == 'escape': application.quit()

app.run()