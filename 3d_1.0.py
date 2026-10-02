from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
import wave
import struct
import os

# --- Procedural Audio Generator ---
# Generates lightweight .wav files so the game runs with zero external asset downloads.
def create_sound_assets():
    sample_rate = 44100

    def write_wav(filename, samples):
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            raw_data = struct.pack('<' + ('h' * len(samples)), *samples)
            wav_file.writeframes(raw_data)

    # 1. Coin Pickup Sound (bright two-tone chime)
    if not os.path.exists('coin.wav'):
        duration = 0.25
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 987.77 if t < 0.1 else 1318.51  # B5 then E6
            amplitude = int(18000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('coin.wav', samples)

    # 2. Jump Sound (ascending pitch sweep)
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

    # 3. Ambient Background Music (gentle looping synth drone)
    if not os.path.exists('bgm.wav'):
        duration = 4.0
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            # Harmonic layering around C3 (130.81 Hz) and G3 (196.00 Hz)
            wave1 = math.sin(2 * math.pi * 130.81 * t)
            wave2 = 0.5 * math.sin(2 * math.pi * 196.00 * t)
            wave3 = 0.25 * math.sin(2 * math.pi * 261.63 * t)
            combined = (wave1 + wave2 + wave3) / 1.75
            val = int(7000 * combined)
            samples.append(max(min(val, 32767), -32768))
        write_wav('bgm.wav', samples)

create_sound_assets()

# --- Game Engine Initialization ---
app = Ursina()

window.title = "3D Coin Collector - Audio Enabled"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# --- Audio Setup ---
# Background Music: starts playing immediately, loops indefinitely
bgm = Audio('bgm.wav', loop=True, autoplay=True, volume=0.4)

# Preloaded Sound Effects: autoplay=False so they trigger on specific events
coin_sfx = Audio('coin.wav', autoplay=False, loop=False, volume=0.7)
jump_sfx = Audio('jump.wav', autoplay=False, loop=False, volume=0.6)

# Lighting
DirectionalLight(y=2, z=-1, shadows=True, rotation=(45, -45, 45))
AmbientLight(color=color.rgba(100, 100, 100, 0.5))

# Ground Plane
ground = Entity(
    model='plane',
    scale=(64, 1, 64),
    color=color.hex('#2d5a27'),
    texture='white_cube',
    texture_scale=(64, 64),
    collider='box'
)

# Boundary Walls
wall_thickness = 1
wall_height = 4
arena_size = 32

walls = [
    Entity(model='cube', scale=(arena_size * 2, wall_height, wall_thickness), position=(0, wall_height / 2, arena_size), color=color.dark_gray, collider='box'),
    Entity(model='cube', scale=(arena_size * 2, wall_height, wall_thickness), position=(0, wall_height / 2, -arena_size), color=color.dark_gray, collider='box'),
    Entity(model='cube', scale=(wall_thickness, wall_height, arena_size * 2), position=(arena_size, wall_height / 2, 0), color=color.dark_gray, collider='box'),
    Entity(model='cube', scale=(wall_thickness, wall_height, arena_size * 2), position=(-arena_size, wall_height / 2, 0), color=color.dark_gray, collider='box'),
]

# Random Obstacles
for _ in range(12):
    x_pos = random.uniform(-25, 25)
    z_pos = random.uniform(-25, 25)
    Entity(
        model='cube',
        position=(x_pos, 2, z_pos),
        scale=(2, 4, 2),
        color=color.hex('#4a4a4a'),
        collider='box'
    )

# Player Setup
player = FirstPersonController(
    speed=8,
    jump_height=1.5,
    origin_y=-0.5,
    position=(0, 2, 0)
)
player.cursor.color = color.white

# UI Score Tracker
score = 0
score_text = Text(
    text=f'Coins Collected: {score}',
    position=(-0.85, 0.45),
    scale=1.5,
    color=color.yellow
)

# Collectibles (Coins)
coins = []

def spawn_coin():
    x = random.uniform(-25, 25)
    z = random.uniform(-25, 25)
    coin = Entity(
        model='cylinder',
        color=color.gold,
        scale=(0.8, 0.15, 0.8),
        rotation=(90, 0, 0),
        position=(x, 1, z),
        collider='sphere'
    )
    coins.append(coin)

for _ in range(10):
    spawn_coin()

# Frame Update Loop
def update():
    global score

    # Spin all active coins
    for coin in coins:
        coin.rotation_y += 120 * time.dt
        
        # Coin pickup detection
        if distance(player.position, coin.position) < 1.6:
            coin_sfx.play()  # Trigger collection sound effect
            coins.remove(coin)
            destroy(coin)
            score += 1
            score_text.text = f'Coins Collected: {score}'
            spawn_coin()

    # Reset position if player falls out of bounds
    if player.y < -10:
        player.position = (0, 3, 0)

# Input Handler
def input(key):
    # Trigger jump SFX only if player is grounded
    if key == 'space' and player.grounded:
        jump_sfx.play()

    if key == 'escape':
        application.quit()

app.run()