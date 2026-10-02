from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
import wave
import struct
import os

# --- Sound Synthesis ---
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

    # Laser/Blaster gunshot sound effect
    if not os.path.exists('shoot.wav'):
        duration = 0.18
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            # Rapid pitch drop from 1200 Hz down to 100 Hz
            freq = 1200 * math.exp(-22 * t) + 100
            amplitude = int(22000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('shoot.wav', samples)

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

window.title = "3D Ruins - First Person Shooter"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

Sky(color=color.hex('#87CEEB'))
scene.fog_density = 0.02
scene.fog_color = color.hex('#a3c2c2')

sun = DirectionalLight(y=20, z=-10, shadows=True, rotation=(45, -30, 0))
sun.color = color.rgba(255, 250, 230, 255)
AmbientLight(color=color.rgba(90, 100, 110, 200))

# Audio
bgm = Audio('bgm.wav', loop=True, autoplay=True, volume=0.3)
coin_sfx = Audio('coin.wav', autoplay=False, loop=False, volume=0.7)
jump_sfx = Audio('jump.wav', autoplay=False, loop=False, volume=0.6)
shoot_sfx = Audio('shoot.wav', autoplay=False, loop=False, volume=0.8)

# Ground
ground = Entity(
    model='plane',
    scale=(100, 1, 100),
    color=color.hex('#3b6b35'),
    texture='grass',
    texture_scale=(50, 50),
    collider='box'
)

# --- Procedural World Objects ---
class Tree(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        Entity(parent=self, model='cylinder', color=color.hex('#5A3825'), scale=(0.8, 3.5, 0.8), y=1.75, collider='box')
        foliage_layers = [(0, 3.0, 3.8, color.hex('#1d4722')), (0, 4.2, 3.0, color.hex('#265c2c')), (0, 5.4, 2.2, color.hex('#32783a'))]
        for ox, oy, scale_val, col in foliage_layers:
            Entity(parent=self, model='cone', color=col, scale=(scale_val, 2.4, scale_val), y=oy)

class AncientRuin(Entity):
    def __init__(self, position=(0, 0, 0), rotation_y=0):
        super().__init__(position=position, rotation_y=rotation_y)
        stone_col = color.hex('#6e7271')
        moss_col = color.hex('#52574e')
        Entity(parent=self, model='cube', scale=(4, 0.8, 2), y=0.4, color=moss_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.7, 4, 0.7), position=(-1.3, 2.4, 0), color=stone_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.7, 4, 0.7), position=(1.3, 2.4, 0), color=stone_col, collider='box')
        Entity(parent=self, model='cube', scale=(4.2, 0.8, 1.4), y=4.8, color=stone_col, collider='box')

class Guardian(Entity):
    def __init__(self, position=(0, 0, 0), rotation_y=0):
        super().__init__(position=position, rotation_y=rotation_y, name='guardian')
        armor_col = color.hex('#a89f8c')
        skin_col = color.hex('#c2b280')
        accent_col = color.hex('#5e5443')

        Entity(parent=self, model='cube', scale=(0.8, 1.2, 0.5), y=1.6, color=armor_col, collider='box')
        Entity(parent=self, model='sphere', scale=0.5, y=2.4, color=skin_col)
        Entity(parent=self, model='cube', scale=(0.6, 0.1, 0.6), y=2.6, color=accent_col)
        Entity(parent=self, model='cylinder', scale=(0.25, 1.0, 0.25), position=(-0.25, 0.5, 0), color=accent_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.25, 1.0, 0.25), position=(0.25, 0.5, 0), color=accent_col, collider='box')
        Entity(parent=self, model='cylinder', scale=(0.2, 1.1, 0.2), position=(-0.55, 1.6, 0), rotation_z=15, color=armor_col)
        Entity(parent=self, model='cylinder', scale=(0.2, 1.1, 0.2), position=(0.55, 1.6, 0), rotation_z=-15, color=armor_col)

class Altar(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        Entity(parent=self, model='cylinder', scale=(2.2, 0.4, 2.2), y=0.2, color=color.hex('#474747'), collider='box')
        Entity(parent=self, model='cylinder', scale=(1.4, 0.8, 1.4), y=0.8, color=color.hex('#5c5c5c'), collider='box')

# Spawn Environment
for _ in range(35):
    tx = random.uniform(-42, 42)
    tz = random.uniform(-42, 42)
    if distance((tx, 0, tz), (0, 0, 0)) > 6: Tree(position=(tx, 0, tz))

for _ in range(8):
    rx = random.uniform(-38, 38)
    rz = random.uniform(-38, 38)
    if distance((rx, 0, rz), (0, 0, 0)) > 8: AncientRuin(position=(rx, 0, rz), rotation_y=random.randint(0, 360))

for _ in range(6):
    gx = random.uniform(-35, 35)
    gz = random.uniform(-35, 35)
    if distance((gx, 0, gz), (0, 0, 0)) > 10: Guardian(position=(gx, 0, gz), rotation_y=random.randint(0, 360))

wall_dist = 48
wall_height = 5
wall_col = color.hex('#3e4242')
walls = [
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, -wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(wall_dist, wall_height / 2, 0), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(-wall_dist, wall_height / 2, 0), color=wall_col, collider='box')
]

# --- Player & First Person Viewmodel ---
player = FirstPersonController(
    speed=9,
    jump_height=1.6,
    origin_y=-0.5,
    position=(0, 2, 0)
)
# Red reticle in center screen
player.cursor.color = color.rgba(255, 60, 60, 200)
player.cursor.scale = 0.015

# Viewmodel Arm & Weapon Rig (Attached directly to the player camera)
gun_rig = Entity(
    parent=camera,
    position=(0.42, -0.32, 0.75),
    rotation=(0, -5, 0)
)
default_rig_pos = gun_rig.position

# Player Hand/Arm
arm = Entity(
    parent=gun_rig,
    model='cube',
    position=(0.08, -0.15, -0.35),
    scale=(0.14, 0.16, 0.8),
    rotation=(15, -5, 0),
    color=color.hex('#d69f7e')
)

# Weapon Body (Futuristic Blaster)
gun_receiver = Entity(
    parent=gun_rig,
    model='cube',
    position=(0, 0, 0),
    scale=(0.1, 0.14, 0.45),
    color=color.hex('#22252a')
)
gun_barrel = Entity(
    parent=gun_rig,
    model='cylinder',
    position=(0, 0.03, 0.35),
    scale=(0.06, 0.35, 0.06),
    rotation=(90, 0, 0),
    color=color.hex('#101214')
)
gun_glow_strip = Entity(
    parent=gun_rig,
    model='cube',
    position=(0, 0.07, 0.05),
    scale=(0.04, 0.03, 0.3),
    color=color.cyan
)
gun_handle = Entity(
    parent=gun_rig,
    model='cube',
    position=(0, -0.12, -0.1),
    scale=(0.08, 0.22, 0.1),
    rotation=(-20, 0, 0),
    color=color.hex('#353a40')
)

# Dynamic Muzzle Flash
muzzle_flash = Entity(
    parent=gun_rig,
    model='sphere',
    position=(0, 0.03, 0.58),
    scale=0.15,
    color=color.cyan,
    enabled=False
)

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
    coin_root = Entity(position=(x, 1.8, z), base_y=1.8, seed=random.uniform(0, 100))
    Entity(parent=coin_root, model='diamond', scale=(0.9, 1.3, 0.9), color=color.hex('#FFD700'), collider='box')
    Entity(parent=coin_root, model='sphere', scale=0.4, color=color.white)
    active_coins.append(coin_root)

def trigger_particles(pos, col=color.gold, count=12):
    for _ in range(count):
        p = Entity(
            model='cube',
            scale=0.12,
            color=col,
            position=pos + Vec3(random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15), random.uniform(-0.15, 0.15))
        )
        p.velocity = Vec3(random.uniform(-4, 4), random.uniform(2, 6), random.uniform(-4, 4))
        p.lifetime = 0.4
        active_particles.append(p)

for _ in range(12):
    spawn_coin()

# --- Shooting Mechanic ---
can_shoot = True

def hide_flash():
    muzzle_flash.enabled = False

def shoot():
    global can_shoot
    if not can_shoot:
        return

    shoot_sfx.play()

    # Visual Muzzle Flash
    muzzle_flash.enabled = True
    invoke(hide_flash, delay=0.05)

    # Recoil Animation: kicks back and upwards, returns smoothly
    gun_rig.animate_position(default_rig_pos + Vec3(0, 0.04, -0.15), duration=0.04, curve=curve.linear)
    gun_rig.animate_rotation(Vec3(-8, -5, 4), duration=0.04)
    invoke(lambda: gun_rig.animate_position(default_rig_pos, duration=0.15, curve=curve.out_bounce), delay=0.05)
    invoke(lambda: gun_rig.animate_rotation(Vec3(0, -5, 0), duration=0.15), delay=0.05)

    # Raycast from camera center outward
    hit_info = raycast(camera.world_position, camera.forward, distance=60, ignore=[player, gun_rig])

    if hit_info.hit:
        # Spawn hit spark VFX
        trigger_particles(hit_info.world_point, col=color.cyan, count=8)

        # Destructible/reactive targets
        hit_entity = hit_info.entity
        
        # Check if shot a gem
        for c in list(active_coins):
            if hit_entity in c.children or hit_entity == c:
                coin_sfx.play()
                trigger_particles(c.position, col=color.gold, count=16)
                active_coins.remove(c)
                destroy(c)
                global score
                score += 1
                score_text.text = f'Gems: {score}'
                spawn_coin()
                break

        # Check if shot a guardian
        if hit_entity.parent and getattr(hit_entity.parent, 'name', '') == 'guardian':
            trigger_particles(hit_info.world_point, col=color.smoke, count=10)
            # Recoil guardian slightly backward
            hit_entity.parent.z += camera.forward.z * 0.3
            hit_entity.parent.x += camera.forward.x * 0.3

# --- Frame Loop ---
def update():
    global score

    # Gem bobbing and proximity pickup
    for coin in list(active_coins):
        coin.rotation_y += 90 * time.dt
        coin.y = coin.base_y + math.sin(time.time() * 3 + coin.seed) * 0.25

        if distance(player.position, coin.position) < 1.7:
            coin_sfx.play()
            trigger_particles(coin.position, col=color.gold, count=14)
            active_coins.remove(coin)
            destroy(coin)
            score += 1
            score_text.text = f'Gems: {score}'
            spawn_coin()

    # Particle simulation
    for p in list(active_particles):
        p.position += p.velocity * time.dt
        p.velocity.y -= 14 * time.dt
        p.scale *= 0.92
        p.lifetime -= time.dt
        if p.lifetime <= 0:
            active_particles.remove(p)
            destroy(p)

    # Subtle weapon sway when walking
    if player.moving:
        sway_x = math.sin(time.time() * 10) * 0.015
        sway_y = math.cos(time.time() * 20) * 0.012
        gun_rig.x = default_rig_pos.x + sway_x
        gun_rig.y = default_rig_pos.y + sway_y
    else:
        # Breathing idle sway
        gun_rig.y = default_rig_pos.y + math.sin(time.time() * 2) * 0.004

    # Boundary reset
    if player.y < -15:
        player.position = (0, 3, 0)

# Input handling
def input(key):
    # Left mouse click to shoot
    if key == 'left mouse down':
        shoot()

    if key == 'space' and player.grounded:
        jump_sfx.play()

    if key == 'escape':
        application.quit()

app.run()