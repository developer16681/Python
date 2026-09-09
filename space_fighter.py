import math
import random
import struct
import wave
from pathlib import Path
from ursina import *

# ==========================================
# 0. PROCEDURAL SOUND & MUSIC GENERATOR
# ==========================================
# Generates .wav files using standard library math/wave if missing.


def create_wav(filename, duration, sample_rate, wave_func):
    filepath = Path(filename)
    if filepath.exists():
        return
    num_samples = int(duration * sample_rate)
    with wave.open(str(filepath), "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for i in range(num_samples):
            t = i / sample_rate
            value = wave_func(t, duration)
            packed_val = struct.pack("<h", max(-32768, min(32767, value)))
            frames.extend(packed_val)
        wav_file.writeframes(frames)


sr = 22050

# 1. Laser Sound (Frequency sweep down)
create_wav(
    "laser_snd.wav",
    0.15,
    sr,
    lambda t, d: int(
        32000
        * (1 - t / d)
        * math.sin(2 * math.pi * (800 - (t / d) * 500) * t)
    ),
)

# 2. Explosion Sound (Noise decay)
create_wav(
    "explosion_snd.wav",
    0.35,
    sr,
    lambda t, d: int(
        32000 * (1 - t / d) ** 2 * (random.random() * 2 - 1)
    ),
)

# 3. Hit Sound (Distorted pulse)
create_wav(
    "hit_snd.wav",
    0.25,
    sr,
    lambda t, d: int(
        28000 * (1 - t / d) * math.sin(2 * math.pi * 180 * t)
        + 10000 * (random.random() * 2 - 1)
    ),
)

# 4. Background Synth Track (Retro Arpeggio Loop)
notes = [130.81, 155.56, 174.61, 196.00, 233.08, 196.00]  # C, Eb, F, G, Bb, G


def music_synth(t, d):
    note_idx = int((t * 6) % len(notes))
    freq = notes[note_idx]
    env = 1.0 - ((t * 6) % 1.0)
    # Sawtooth wave blended with sine sub-bass
    saw = 2 * ((t * freq) % 1) - 1
    sub = math.sin(2 * math.pi * (freq / 2) * t)
    return int(12000 * env * (0.6 * saw + 0.4 * sub))


create_wav("bg_music.wav", 8.0, sr, music_synth)

# ==========================================
# 1. APPLICATION & WINDOW SETUP
# ==========================================
app = Ursina()

window.title = "3D Starfighter: Galactic Pursuit"
window.borderless = False
window.fullscreen = False
window.fps_counter.enabled = True

# ==========================================
# 2. PROCEDURAL 3D MESH DEFINITIONS
# ==========================================


def create_cone_mesh(radius=0.5, height=2.0, sides=8):
    verts = []
    triangles = []

    # Apex
    apex = Vec3(0, 0, height / 2)
    base_center = Vec3(0, 0, -height / 2)
    verts.append(apex)  # Index 0
    verts.append(base_center)  # Index 1

    for i in range(sides):
        angle = (i / sides) * 2 * math.pi
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        verts.append(Vec3(x, y, -height / 2))

    for i in range(sides):
        curr_idx = 2 + i
        next_idx = 2 + ((i + 1) % sides)
        # Side face
        triangles.append((0, next_idx, curr_idx))
        # Base face
        triangles.append((1, curr_idx, next_idx))

    return Mesh(vertices=verts, triangles=triangles, mode="triangle")


def create_octahedron_mesh(size=1.0):
    s = size / 2.0
    verts = [
        Vec3(0, s, 0),  # Top (0)
        Vec3(0, -s, 0),  # Bottom (1)
        Vec3(-s, 0, 0),  # Left (2)
        Vec3(s, 0, 0),  # Right (3)
        Vec3(0, 0, s),  # Front (4)
        Vec3(0, 0, -s),  # Back (5)
    ]
    triangles = [
        # Top pyramid
        (0, 4, 3),
        (0, 3, 5),
        (0, 5, 2),
        (0, 2, 4),
        # Bottom pyramid
        (1, 3, 4),
        (1, 5, 3),
        (1, 2, 5),
        (1, 4, 2),
    ]
    return Mesh(vertices=verts, triangles=triangles, mode="triangle")


# Pre-generate Meshes
cone_mesh = create_cone_mesh()
octahedron_mesh = create_octahedron_mesh()

# ==========================================
# 3. GAME STATE & AUDIO LOOPS
# ==========================================
score = 0
health = 100
game_over = False

# Background Synth Music (Looping)
bg_audio = Audio("bg_music.wav", loop=True, volume=0.45, autoplay=True)

# HUD Overlay
score_text = Text(
    text="SCORE: 0", position=(-0.85, 0.45), scale=2, color=color.cyan
)
health_text = Text(
    text="HEALTH: 100%", position=(0.55, 0.45), scale=2, color=color.green
)
crosshair = Entity(
    model="quad",
    texture="circle",
    scale=0.025,
    color=color.rgba(255, 255, 255, 180),
)

# Environment & Starfield
Sky(color=color.black)

for _ in range(350):
    Entity(
        model="sphere",
        position=(
            random.uniform(-200, 200),
            random.uniform(-200, 200),
            random.uniform(-200, 200),
        ),
        scale=random.uniform(0.1, 0.35),
        color=color.white,
    )

# Player Ship
player = Entity(
    model=cone_mesh,
    color=color.azure,
    scale=(0.8, 0.4, 1.5),
    position=(0, 0, 0),
)

# Chase Camera
camera.parent = player
camera.position = (0, 2.5, -9)
camera.rotation_x = 10

lasers = []
enemies = []
particles = []

# ==========================================
# 4. ENTITY CLASSES
# ==========================================


class Enemy(Entity):

    def __init__(self, position):
        super().__init__(
            model=octahedron_mesh,
            color=color.red,
            position=position,
            scale=(1.8, 1.8, 1.8),
            collider="box",
        )
        self.speed = random.uniform(12, 22)

    def update(self):
        if game_over:
            return

        self.look_at(player)
        self.position += self.forward * self.speed * time.dt

        # Collision with Player
        if self.intersects(player).hit:
            global health
            health -= 25
            health_text.text = f"HEALTH: {max(0, health)}%"

            if health <= 50:
                health_text.color = color.orange
            if health <= 20:
                health_text.color = color.red

            Audio("hit_snd.wav", volume=0.8, auto_destroy=True)
            create_explosion(self.position, color.red)

            if self in enemies:
                enemies.remove(self)
                destroy(self)

            if health <= 0:
                trigger_game_over()


class Laser(Entity):

    def __init__(self, position, rotation):
        super().__init__(
            model="cube",
            color=color.yellow,
            position=position,
            rotation=rotation,
            scale=(0.1, 0.1, 1.8),
            collider="box",
        )
        self.speed = 95

    def update(self):
        self.position += self.forward * self.speed * time.dt

        # Collision with Enemy
        hit_info = self.intersects()
        if hit_info.hit and hit_info.entity in enemies:
            global score
            enemy = hit_info.entity
            score += 100
            score_text.text = f"SCORE: {score}"

            Audio("explosion_snd.wav", volume=0.7, auto_destroy=True)
            create_explosion(enemy.position, color.yellow)

            if enemy in enemies:
                enemies.remove(enemy)
                destroy(enemy)

            if self in lasers:
                lasers.remove(self)
                destroy(self)

        elif distance(self.position, player.position) > 130:
            if self in lasers:
                lasers.remove(self)
                destroy(self)


def create_explosion(pos, col):
    for _ in range(14):
        p = Entity(
            model="cube",
            position=pos,
            scale=random.uniform(0.1, 0.35),
            color=col,
        )
        p.velocity = Vec3(
            random.uniform(-6, 6), random.uniform(-6, 6), random.uniform(-6, 6)
        )
        particles.append((p, time.time()))


def trigger_game_over():
    global game_over
    game_over = True
    bg_audio.volume = 0.15
    Text(text="SYSTEM DESTROYED", origin=(0, 0), scale=4, color=color.red)
    Text(
        text="Press [R] to Restart", origin=(0, 2), scale=2, color=color.white
    )


# ==========================================
# 5. INPUT & GAME LOOP
# ==========================================


def input(key):
    if key == "space" or key == "left mouse down":
        if not game_over:
            l1 = Laser(
                player.position
                + player.right * 0.9
                + player.forward * 1.2,
                player.rotation,
            )
            l2 = Laser(
                player.position
                - player.right * 0.9
                + player.forward * 1.2,
                player.rotation,
            )
            lasers.extend([l1, l2])
            Audio("laser_snd.wav", volume=0.5, auto_destroy=True)

    if key == "r" and game_over:
        restart_game()


def restart_game():
    global score, health, game_over
    score = 0
    health = 100
    game_over = False
    bg_audio.volume = 0.45
    score_text.text = "SCORE: 0"
    health_text.text = "HEALTH: 100%"
    health_text.color = color.green

    for e in enemies[:]:
        destroy(e)
    enemies.clear()

    for l in lasers[:]:
        destroy(l)
    lasers.clear()

    player.position = (0, 0, 0)
    player.rotation = (0, 0, 0)


spawn_timer = 0


def update():
    global spawn_timer
    if game_over:
        return

    # Flight Controls
    pitch = held_keys["s"] - held_keys["w"]
    yaw = held_keys["d"] - held_keys["a"]
    roll = held_keys["q"] - held_keys["e"]

    player.rotation_x += pitch * 65 * time.dt
    player.rotation_y += yaw * 65 * time.dt
    player.rotation_z += roll * 90 * time.dt

    player.position += player.forward * 18 * time.dt

    # Spawning
    spawn_timer += time.dt
    if spawn_timer > 1.1:
        spawn_timer = 0
        spawn_pos = (
            player.position
            + player.forward * random.uniform(70, 100)
            + Vec3(random.uniform(-30, 30), random.uniform(-30, 30), 0)
        )
        enemies.append(Enemy(spawn_pos))

    # Particle Animations
    for p, spawn_time in particles[:]:
        p.position += p.velocity * time.dt
        p.scale *= 0.91
        if time.time() - spawn_time > 0.4:
            particles.remove((p, spawn_time))
            destroy(p)


app.run()