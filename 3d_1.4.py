from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math
import wave
import struct
import os

# --- Procedural Audio Generator ---
def create_sound_assets():
    sample_rate = 44100

    def write_wav(filename, samples):
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            raw_data = struct.pack('<' + ('h' * len(samples)), *samples)
            wav_file.writeframes(raw_data)

    # Gem Pickup Sound
    if not os.path.exists('coin.wav'):
        duration = 0.22
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 987.77 if t < 0.09 else 1318.51
            amplitude = int(18000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('coin.wav', samples)

    # Jump Sound
    if not os.path.exists('jump.wav'):
        duration = 0.2
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 180 + (t / duration) * 320
            amplitude = int(14000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('jump.wav', samples)

    # Weapon 1: Pistol Sound (Punchy energy pop)
    if not os.path.exists('shoot_pistol.wav'):
        duration = 0.16
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 950 * math.exp(-20 * t) + 120
            amplitude = int(22000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('shoot_pistol.wav', samples)

    # Weapon 2: Shotgun Sound (Deep explosive boom with noise)
    if not os.path.exists('shoot_shotgun.wav'):
        duration = 0.38
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 240 * math.exp(-12 * t) + 40
            noise = (random.random() * 2 - 1) * 0.45
            tonal = math.sin(2 * math.pi * freq * t)
            amplitude = int(28000 * (1 - (t / duration)))
            val = int(amplitude * (tonal * 0.55 + noise))
            samples.append(max(min(val, 32767), -32768))
        write_wav('shoot_shotgun.wav', samples)

    # Weapon 3: SMG Sound (Snappy rapid cyclic crack)
    if not os.path.exists('shoot_smg.wav'):
        duration = 0.08
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 1400 * math.exp(-35 * t) + 200
            amplitude = int(19000 * (1 - (t / duration)))
            val = int(amplitude * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('shoot_smg.wav', samples)

    # Weapon Switch Click
    if not os.path.exists('switch.wav'):
        duration = 0.06
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 1800 if t < 0.03 else 2400
            val = int(12000 * math.sin(2 * math.pi * freq * t))
            samples.append(max(min(val, 32767), -32768))
        write_wav('switch.wav', samples)

    # Looping Ambient Music
    if not os.path.exists('bgm.wav'):
        duration = 4.0
        samples = []
        n_samples = int(sample_rate * duration)
        for i in range(n_samples):
            t = i / sample_rate
            w1 = math.sin(2 * math.pi * 130.81 * t)
            w2 = 0.5 * math.sin(2 * math.pi * 196.00 * t)
            w3 = 0.25 * math.sin(2 * math.pi * 261.63 * t)
            val = int(6000 * ((w1 + w2 + w3) / 1.75))
            samples.append(max(min(val, 32767), -32768))
        write_wav('bgm.wav', samples)

create_sound_assets()

# --- Engine Setup ---
app = Ursina()

# Procedural Meshes
cylinder_mesh = Cylinder(resolution=12)
cone_mesh = Cone(resolution=12)

window.title = "3D Arsenal - Multi-Weapon FPS"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

Sky(color=color.hex('#87CEEB'))
scene.fog_density = 0.02
scene.fog_color = color.hex('#a3c2c2')

sun = DirectionalLight(y=20, z=-10, shadows=True, rotation=(45, -30, 0))
sun.color = color.rgba(255, 250, 230, 255)
AmbientLight(color=color.rgba(90, 100, 110, 200))

# Audio Instances
bgm = Audio('bgm.wav', loop=True, autoplay=True, volume=0.3)
coin_sfx = Audio('coin.wav', autoplay=False, loop=False, volume=0.7)
jump_sfx = Audio('jump.wav', autoplay=False, loop=False, volume=0.6)
switch_sfx = Audio('switch.wav', autoplay=False, loop=False, volume=0.6)

# Ground
Entity(
    model='plane',
    scale=(100, 1, 100),
    color=color.hex('#3b6b35'),
    texture='grass',
    texture_scale=(50, 50),
    collider='box'
)

# --- World Scenery ---
class Tree(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        Entity(parent=self, model=cylinder_mesh, color=color.hex('#5A3825'), scale=(0.8, 3.5, 0.8), y=1.75, collider='box')
        foliage_layers = [(0, 3.0, 3.8, color.hex('#1d4722')), (0, 4.2, 3.0, color.hex('#265c2c')), (0, 5.4, 2.2, color.hex('#32783a'))]
        for ox, oy, scale_val, col in foliage_layers:
            Entity(parent=self, model=cone_mesh, color=col, scale=(scale_val, 2.4, scale_val), y=oy)

class AncientRuin(Entity):
    def __init__(self, position=(0, 0, 0), rotation_y=0):
        super().__init__(position=position, rotation_y=rotation_y)
        stone_col = color.hex('#6e7271')
        moss_col = color.hex('#52574e')
        Entity(parent=self, model='cube', scale=(4, 0.8, 2), y=0.4, color=moss_col, collider='box')
        Entity(parent=self, model=cylinder_mesh, scale=(0.7, 4, 0.7), position=(-1.3, 2.4, 0), color=stone_col, collider='box')
        Entity(parent=self, model=cylinder_mesh, scale=(0.7, 4, 0.7), position=(1.3, 2.4, 0), color=stone_col, collider='box')
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
        Entity(parent=self, model=cylinder_mesh, scale=(0.25, 1.0, 0.25), position=(-0.25, 0.5, 0), color=accent_col, collider='box')
        Entity(parent=self, model=cylinder_mesh, scale=(0.25, 1.0, 0.25), position=(0.25, 0.5, 0), color=accent_col, collider='box')
        Entity(parent=self, model=cylinder_mesh, scale=(0.2, 1.1, 0.2), position=(-0.55, 1.6, 0), rotation_z=15, color=armor_col)
        Entity(parent=self, model=cylinder_mesh, scale=(0.2, 1.1, 0.2), position=(0.55, 1.6, 0), rotation_z=-15, color=armor_col)

class Altar(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        Entity(parent=self, model=cylinder_mesh, scale=(2.2, 0.4, 2.2), y=0.2, color=color.hex('#474747'), collider='box')
        Entity(parent=self, model=cylinder_mesh, scale=(1.4, 0.8, 1.4), y=0.8, color=color.hex('#5c5c5c'), collider='box')

# Spawn Scenery
for _ in range(35):
    tx, tz = random.uniform(-42, 42), random.uniform(-42, 42)
    if distance((tx, 0, tz), (0, 0, 0)) > 6: Tree(position=(tx, 0, tz))

for _ in range(8):
    rx, rz = random.uniform(-38, 38), random.uniform(-38, 38)
    if distance((rx, 0, rz), (0, 0, 0)) > 8: AncientRuin(position=(rx, 0, rz), rotation_y=random.randint(0, 360))

for _ in range(6):
    gx, gz = random.uniform(-35, 35), random.uniform(-35, 35)
    if distance((gx, 0, gz), (0, 0, 0)) > 10: Guardian(position=(gx, 0, gz), rotation_y=random.randint(0, 360))

# Arena Walls
wall_dist = 48
wall_height = 5
wall_col = color.hex('#3e4242')
walls = [
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(wall_dist * 2, wall_height, 2), position=(0, wall_height / 2, -wall_dist), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(wall_dist, wall_height / 2, 0), color=wall_col, collider='box'),
    Entity(model='cube', scale=(2, wall_height, wall_dist * 2), position=(-wall_dist, wall_height / 2, 0), color=wall_col, collider='box')
]

# --- Player Setup ---
player = FirstPersonController(
    speed=9,
    jump_height=1.6,
    origin_y=-0.5,
    position=(0, 2, 0)
)
player.cursor.color = color.rgba(255, 60, 60, 200)
player.cursor.scale = 0.015

# --- Procedural Weapon Armory Models ---
gun_rig = Entity(parent=camera, position=(0.42, -0.32, 0.75), rotation=(0, -5, 0))
default_rig_pos = gun_rig.position

# Universal Arm
Entity(
    parent=gun_rig,
    model='cube',
    position=(0.08, -0.15, -0.35),
    scale=(0.14, 0.16, 0.8),
    rotation=(15, -5, 0),
    color=color.hex('#d69f7e')
)

# 1. Pistol Model
pistol_root = Entity(parent=gun_rig, enabled=True)
Entity(parent=pistol_root, model='cube', scale=(0.1, 0.14, 0.45), color=color.hex('#22252a'))
Entity(parent=pistol_root, model=cylinder_mesh, position=(0, 0.03, 0.35), scale=(0.06, 0.35, 0.06), rotation=(90, 0, 0), color=color.hex('#101214'))
Entity(parent=pistol_root, model='cube', position=(0, 0.07, 0.05), scale=(0.04, 0.03, 0.3), color=color.cyan)
Entity(parent=pistol_root, model='cube', position=(0, -0.12, -0.1), scale=(0.08, 0.22, 0.1), rotation=(-20, 0, 0), color=color.hex('#353a40'))

# 2. Shotgun Model (Heavy, dual-barrel, wooden pump grip)
shotgun_root = Entity(parent=gun_rig, enabled=False)
Entity(parent=shotgun_root, model='cube', scale=(0.14, 0.16, 0.5), position=(0, 0, -0.05), color=color.hex('#282828'))
# Twin Barrels
Entity(parent=shotgun_root, model=cylinder_mesh, position=(-0.04, 0.05, 0.45), scale=(0.065, 0.65, 0.065), rotation=(90, 0, 0), color=color.hex('#1a1a1a'))
Entity(parent=shotgun_root, model=cylinder_mesh, position=(0.04, 0.05, 0.45), scale=(0.065, 0.65, 0.065), rotation=(90, 0, 0), color=color.hex('#1a1a1a'))
# Wooden Pump & Grip
Entity(parent=shotgun_root, model='cube', position=(0, -0.02, 0.35), scale=(0.12, 0.1, 0.3), color=color.hex('#8B4513'))
Entity(parent=shotgun_root, model='cube', position=(0, -0.16, -0.2), scale=(0.1, 0.26, 0.12), rotation=(-25, 0, 0), color=color.hex('#8B4513'))

# 3. SMG Model (Compact, vertical magazine, top rail sight)
smg_root = Entity(parent=gun_rig, enabled=False)
Entity(parent=smg_root, model='cube', scale=(0.11, 0.18, 0.42), color=color.hex('#1f2326'))
Entity(parent=smg_root, model=cylinder_mesh, position=(0, 0.04, 0.38), scale=(0.05, 0.4, 0.05), rotation=(90, 0, 0), color=color.hex('#393e46'))
# Curved Banana Mag
Entity(parent=smg_root, model='cube', position=(0, -0.25, 0.06), scale=(0.06, 0.35, 0.12), rotation=(15, 0, 0), color=color.hex('#0f1112'))
# Top Sight & Foregrip
Entity(parent=smg_root, model='cube', position=(0, 0.11, -0.05), scale=(0.04, 0.05, 0.22), color=color.hex('#00adb5'))
Entity(parent=smg_root, model=cylinder_mesh, position=(0, -0.15, 0.25), scale=(0.04, 0.18, 0.04), color=color.hex('#1f2326'))

# Dynamic Muzzle Flash
muzzle_flash = Entity(parent=gun_rig, model='sphere', scale=0.18, enabled=False)

# --- Weapon Config & Stats ---
weapons = [
    {
        'name': 'Plasma Pistol',
        'root': pistol_root,
        'sfx': Audio('shoot_pistol.wav', autoplay=False, loop=False, volume=0.8),
        'cooldown': 0.25,
        'recoil_pos': Vec3(0, 0.04, -0.15),
        'recoil_rot': Vec3(-8, -5, 4),
        'flash_pos': Vec3(0, 0.03, 0.6),
        'flash_color': color.cyan,
        'pellets': 1,
        'spread': 0.0,
        'automatic': False
    },
    {
        'name': 'Boomstick Shotgun',
        'root': shotgun_root,
        'sfx': Audio('shoot_shotgun.wav', autoplay=False, loop=False, volume=0.9),
        'cooldown': 0.85,
        'recoil_pos': Vec3(0, 0.10, -0.32),
        'recoil_rot': Vec3(-18, -6, 7),
        'flash_pos': Vec3(0, 0.05, 0.82),
        'flash_color': color.orange,
        'pellets': 8,
        'spread': 0.06,
        'automatic': False
    },
    {
        'name': 'Rapid SMG',
        'root': smg_root,
        'sfx': Audio('shoot_smg.wav', autoplay=False, loop=False, volume=0.7),
        'cooldown': 0.09,
        'recoil_pos': Vec3(0, 0.02, -0.08),
        'recoil_rot': Vec3(-3, -2, 2),
        'flash_pos': Vec3(0, 0.04, 0.62),
        'flash_color': color.yellow,
        'pellets': 1,
        'spread': 0.015,
        'automatic': True
    }
]

current_weapon_idx = 0
time_since_shot = 0.0

# --- HUD Overlays ---
score = 0
score_panel = Entity(parent=camera.ui, model='quad', scale=(0.32, 0.08), position=(-0.68, 0.43), color=color.rgba(0, 0, 0, 140))
score_text = Text(parent=camera.ui, text=f'Gems: {score}', position=(-0.82, 0.45), scale=1.4, color=color.gold)

weapon_panel = Entity(parent=camera.ui, model='quad', scale=(0.36, 0.07), position=(0.66, -0.44), color=color.rgba(0, 0, 0, 160))
weapon_text = Text(parent=camera.ui, text=f'[1] {weapons[0]["name"]}', position=(0.50, -0.42), scale=1.1, color=color.cyan)

# --- Switch Weapon Function ---
def switch_weapon(new_index):
    global current_weapon_idx
    if new_index == current_weapon_idx or not (0 <= new_index < len(weapons)):
        return

    # Disable old weapon model, enable new
    weapons[current_weapon_idx]['root'].enabled = False
    current_weapon_idx = new_index
    current_wep = weapons[current_weapon_idx]
    current_wep['root'].enabled = True

    switch_sfx.play()

    # Weapon switch dip animation
    gun_rig.y = default_rig_pos.y - 0.2
    gun_rig.animate_position(default_rig_pos, duration=0.15, curve=curve.out_quad)

    # Update UI Label and Color
    color_map = [color.cyan, color.orange, color.yellow]
    weapon_text.text = f'[{current_weapon_idx + 1}] {current_wep["name"]}'
    weapon_text.color = color_map[current_weapon_idx]

# --- Collectibles & Particles ---
active_coins = []
active_particles = []

def spawn_coin():
    x, z = random.uniform(-40, 40), random.uniform(-40, 40)
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

def hide_flash():
    muzzle_flash.enabled = False

# --- Firing Mechanics ---
def fire_weapon():
    global time_since_shot, score
    current_wep = weapons[current_weapon_idx]

    if time_since_shot < current_wep['cooldown']:
        return

    time_since_shot = 0.0
    current_wep['sfx'].play()

    # Muzzle flash
    muzzle_flash.position = current_wep['flash_pos']
    muzzle_flash.color = current_wep['flash_color']
    muzzle_flash.enabled = True
    invoke(hide_flash, delay=0.04)

    # Recoil
    gun_rig.animate_position(default_rig_pos + current_wep['recoil_pos'], duration=0.03, curve=curve.linear)
    gun_rig.animate_rotation(current_wep['recoil_rot'], duration=0.03)
    invoke(lambda: gun_rig.animate_position(default_rig_pos, duration=0.14, curve=curve.out_bounce), delay=0.04)
    invoke(lambda: gun_rig.animate_rotation(Vec3(0, -5, 0), duration=0.14), delay=0.04)

    # Raycast shot(s)
    pellet_count = current_wep['pellets']
    spread_amt = current_wep['spread']

    for _ in range(pellet_count):
        # Calculate aim direction with spread
        spread_vec = Vec3(
            random.uniform(-spread_amt, spread_amt),
            random.uniform(-spread_amt, spread_amt),
            random.uniform(-spread_amt, spread_amt)
        )
        fire_dir = (camera.forward + spread_vec).normalized()

        hit_info = raycast(camera.world_position, fire_dir, distance=65, ignore=[player, gun_rig])

        if hit_info.hit:
            trigger_particles(hit_info.world_point, col=current_wep['flash_color'], count=6)
            hit_entity = hit_info.entity

            # Shot Gem
            for c in list(active_coins):
                if hit_entity in c.children or hit_entity == c:
                    coin_sfx.play()
                    trigger_particles(c.position, col=color.gold, count=16)
                    active_coins.remove(c)
                    destroy(c)
                    score += 1
                    score_text.text = f'Gems: {score}'
                    spawn_coin()
                    break

            # Shot Guardian
            if hit_entity.parent and getattr(hit_entity.parent, 'name', '') == 'guardian':
                trigger_particles(hit_info.world_point, col=color.smoke, count=10)
                hit_entity.parent.z += fire_dir.z * (0.8 if pellet_count > 1 else 0.3)
                hit_entity.parent.x += fire_dir.x * (0.8 if pellet_count > 1 else 0.3)

# --- Frame Update Loop ---
def update():
    global score, time_since_shot
    time_since_shot += time.dt
    current_wep = weapons[current_weapon_idx]

    # Automatic rapid fire for weapons like SMG when holding left mouse
    if current_wep['automatic'] and mouse.left:
        fire_weapon()

    # Gem bobbing
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

    # Particle physics
    for p in list(active_particles):
        p.position += p.velocity * time.dt
        p.velocity.y -= 14 * time.dt
        p.scale *= 0.92
        p.lifetime -= time.dt
        if p.lifetime <= 0:
            active_particles.remove(p)
            destroy(p)

    # First person weapon sway
    is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']
    if is_moving and player.grounded:
        sway_x = math.sin(time.time() * 10) * 0.015
        sway_y = math.cos(time.time() * 20) * 0.012
        gun_rig.x = default_rig_pos.x + sway_x
        gun_rig.y = default_rig_pos.y + sway_y
    else:
        gun_rig.y = default_rig_pos.y + math.sin(time.time() * 2) * 0.004

    # Boundary Reset
    if player.y < -15:
        player.position = (0, 3, 0)

# --- Input Handling ---
def input(key):
    # Single-fire weapon trigger
    if key == 'left mouse down':
        if not weapons[current_weapon_idx]['automatic']:
            fire_weapon()

    # Weapon Slot Hotkeys
    if key == '1': switch_weapon(0)
    if key == '2': switch_weapon(1)
    if key == '3': switch_weapon(2)

    # Scroll Wheel Cycle
    if key == 'scroll up':
        switch_weapon((current_weapon_idx - 1) % len(weapons))
    if key == 'scroll down':
        switch_weapon((current_weapon_idx + 1) % len(weapons))

    # Jump & Quit
    if key == 'space' and player.grounded:
        jump_sfx.play()

    if key == 'escape':
        application.quit()

app.run()