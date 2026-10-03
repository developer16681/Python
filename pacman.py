"""Pac-Man-inspired arcade game. Install pygame with: python -m pip install pygame"""

import io
import math
import random
import struct
import wave

import pygame


pygame.init()

TILE = 48
MAZE = [
    "###########",
    "#.........#",
    "#.###.###.#",
    "#o#...#...#",
    "#.#.#.###.#",
    "#...#.....#",
    "###.#.###.#",
    "#...#...#o#",
    "#.###.#.#.#",
    "#.........#",
    "###########",
]
ROWS, COLS = len(MAZE), len(MAZE[0])
HUD_WIDTH = 220
WIDTH, HEIGHT = COLS * TILE + HUD_WIDTH, ROWS * TILE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PAC-MAN | Maze Run")
clock = pygame.time.Clock()

BG = (7, 10, 27)
BLUE = (43, 102, 255)
CYAN = (71, 224, 255)
YELLOW = (255, 222, 48)
WHITE = (242, 247, 255)
DIM = (137, 156, 193)
PINK = (255, 77, 151)
ORANGE = (255, 165, 53)
GREEN = (77, 255, 166)
FONT = pygame.font.SysFont("arial", 21, bold=True)
SMALL = pygame.font.SysFont("arial", 16, bold=True)
BIG = pygame.font.SysFont("arial", 42, bold=True)

KEY_DIRS = {
    pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
    pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
    pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
    pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
}
DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def make_tone(frequency, duration, volume=0.16, slide=0):
    """Create a short sound effect in memory; no sound files are needed."""
    rate = 22050
    count = int(rate * duration)
    samples = bytearray()
    for i in range(count):
        t = i / rate
        envelope = min(1.0, i / 180, (count - i) / 400)
        hz = frequency + slide * t
        value = int(32767 * volume * envelope * math.sin(2 * math.pi * hz * t))
        samples.extend(struct.pack("<h", value))
    data = io.BytesIO()
    with wave.open(data, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(samples)
    data.seek(0)
    return pygame.mixer.Sound(file=data)


try:
    pygame.mixer.init()
    SOUNDS = {
        "dot": make_tone(760, 0.055, 0.12, -220),
        "power": make_tone(390, 0.28, 0.2, 750),
        "ghost": make_tone(240, 0.24, 0.2, 480),
        "death": make_tone(500, 0.6, 0.2, -400),
    }
except (pygame.error, OSError):
    SOUNDS = {}


def sound(name):
    if name in SOUNDS:
        SOUNDS[name].play()


def center(tile):
    return tile[0] * TILE + TILE // 2, tile[1] * TILE + TILE // 2


def open_tile(x, y):
    return 0 <= x < COLS and 0 <= y < ROWS and MAZE[y][x] != "#"


def new_game():
    return {
        "dots": {(x, y) for y, row in enumerate(MAZE) for x, cell in enumerate(row)
                 if cell in ".o"},
        "player": list(center((1, 1))), "direction": (0, 0), "queued": (0, 0),
        "mouth": 0.0, "score": 0, "lives": 3, "power": 0.0,
        "started": False, "paused": False, "over": False, "won": False,
        "ghosts": [
            {"pos": list(center(tile)), "dir": (0, 0), "color": color,
             "think": random.uniform(0.1, 0.5)}
            for tile, color in [((5, 3), PINK), ((7, 5), CYAN), ((5, 9), ORANGE)]
        ],
    }


game = new_game()


def tile_at(pos):
    return round((pos[0] - TILE / 2) / TILE), round((pos[1] - TILE / 2) / TILE)


def centered(pos):
    x, y = tile_at(pos)
    cx, cy = center((x, y))
    return abs(pos[0] - cx) < 2.5 and abs(pos[1] - cy) < 2.5


def can_move(pos, direction):
    x, y = tile_at(pos)
    return open_tile(x + direction[0], y + direction[1])


def update_player(dt):
    pos = game["player"]
    if centered(pos):
        x, y = tile_at(pos)
        pos[:] = center((x, y))
        if game["queued"] != (0, 0) and can_move(pos, game["queued"]):
            game["direction"] = game["queued"]
        if not can_move(pos, game["direction"]):
            game["direction"] = (0, 0)

        tile = (x, y)
        if tile in game["dots"]:
            game["dots"].remove(tile)
            if MAZE[y][x] == "o":
                game["score"] += 50
                game["power"] = 8.0
                sound("power")
            else:
                game["score"] += 10
                sound("dot")
            if not game["dots"]:
                game["won"] = True

    dx, dy = game["direction"]
    pos[0] += dx * 178 * dt
    pos[1] += dy * 178 * dt
    game["mouth"] += dt * 11


def update_ghost(ghost, dt):
    pos = ghost["pos"]
    if centered(pos):
        x, y = tile_at(pos)
        pos[:] = center((x, y))
        options = [d for d in DIRS if open_tile(x + d[0], y + d[1])]
        reverse = (-ghost["dir"][0], -ghost["dir"][1])
        choices = [d for d in options if d != reverse] or options
        if choices:
            if game["power"] > 0:
                px, py = game["player"]
                ghost["dir"] = max(choices, key=lambda d: (
                    (x + d[0] - (px - TILE / 2) / TILE) ** 2
                    + (y + d[1] - (py - TILE / 2) / TILE) ** 2
                    + random.random() * 0.15
                ))
            elif ghost["think"] <= 0 or ghost["dir"] not in options:
                ghost["dir"] = random.choice(choices)
                ghost["think"] = random.uniform(0.2, 0.8)
        else:
            ghost["dir"] = (0, 0)
    ghost["think"] -= dt
    speed = 112 if game["power"] <= 0 else 82
    pos[0] += ghost["dir"][0] * speed * dt
    pos[1] += ghost["dir"][1] * speed * dt


def reset_positions():
    game["player"][:] = center((1, 1))
    game["direction"] = (0, 0)
    for ghost, tile in zip(game["ghosts"], ((5, 3), (7, 5), (5, 9))):
        ghost["pos"][:] = center(tile)
        ghost["dir"] = (0, 0)
        ghost["think"] = 0


def update(dt):
    if not game["started"] or game["paused"] or game["over"] or game["won"]:
        return
    game["power"] = max(0.0, game["power"] - dt)
    update_player(dt)
    for ghost in game["ghosts"]:
        update_ghost(ghost, dt)
        dx = ghost["pos"][0] - game["player"][0]
        dy = ghost["pos"][1] - game["player"][1]
        if dx * dx + dy * dy < (TILE * 0.48) ** 2:
            if game["power"] > 0:
                game["score"] += 200
                sound("ghost")
                ghost["pos"][:] = center((5, 5))
                ghost["dir"] = (0, 0)
                ghost["think"] = 0.5
            else:
                game["lives"] -= 1
                sound("death")
                if game["lives"] <= 0:
                    game["over"] = True
                else:
                    reset_positions()
                break


def draw_maze():
    screen.fill(BG)
    for y, row in enumerate(MAZE):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
            if cell == "#":
                pygame.draw.rect(screen, (13, 25, 68), rect.inflate(-2, -2), border_radius=9)
                pygame.draw.rect(screen, BLUE, rect.inflate(-5, -5), 2, border_radius=8)
            elif (x, y) in game["dots"]:
                px, py = center((x, y))
                if cell == "o":
                    pygame.draw.circle(screen, (255, 245, 185), (px, py), 8)
                    pygame.draw.circle(screen, YELLOW, (px, py), 5)
                else:
                    pygame.draw.circle(screen, (255, 225, 180), (px, py), 3)


def draw_player():
    x, y = map(int, game["player"])
    radius = TILE // 2 - 5
    pygame.draw.circle(screen, (130, 94, 0), (x + 2, y + 3), radius)
    pygame.draw.circle(screen, YELLOW, (x, y), radius)
    dx, dy = game["direction"]
    angle = math.atan2(dy, dx) if (dx, dy) != (0, 0) else 0
    opening = 0.1 + abs(math.sin(game["mouth"])) * 0.42
    p1 = (x + math.cos(angle - opening) * radius, y + math.sin(angle - opening) * radius)
    p2 = (x + math.cos(angle + opening) * radius, y + math.sin(angle + opening) * radius)
    pygame.draw.polygon(screen, BG, [(x, y), p1, p2])


def draw_ghost(ghost):
    x, y = map(int, ghost["pos"])
    radius = TILE // 2 - 6
    color = (66, 100, 255) if game["power"] > 0 else ghost["color"]
    pygame.draw.circle(screen, color, (x, y - 3), radius)
    pygame.draw.rect(screen, color, (x - radius, y - 3, radius * 2, radius + 7))
    for i in range(3):
        cx = x - radius + int((i + 0.5) * radius * 2 / 3)
        pygame.draw.circle(screen, color, (cx, y + radius), radius // 3)
    for ex in (x - 7, x + 7):
        pygame.draw.ellipse(screen, WHITE, (ex - 5, y - 12, 10, 14))
        pygame.draw.circle(screen, (25, 43, 105),
                           (ex + ghost["dir"][0] * 2, y - 5 + ghost["dir"][1] * 2), 3)
    if game["power"] > 0:
        pygame.draw.line(screen, WHITE, (x - 11, y - 14), (x - 7, y - 11), 2)
        pygame.draw.line(screen, WHITE, (x + 7, y - 11), (x + 11, y - 14), 2)


def text(message, font, color, x, y):
    screen.blit(font.render(message, True, color), (x, y))


def draw_hud():
    left = COLS * TILE + 22
    pygame.draw.line(screen, (31, 47, 85), (left - 14, 24), (left - 14, HEIGHT - 24), 2)
    text("MAZE RUN", SMALL, CYAN, left, 38)
    text("PAC-MAN", BIG, YELLOW, left, 63)
    text("SCORE", SMALL, DIM, left, 137)
    text(f"{game['score']:06d}", BIG, WHITE, left, 158)
    text("LIVES", SMALL, DIM, left, 226)
    for i in range(game["lives"]):
        cx = left + 16 + i * 35
        pygame.draw.circle(screen, YELLOW, (cx, 267), 13)
        pygame.draw.polygon(screen, BG, [(cx, 267), (cx + 14, 260), (cx + 14, 274)])
    text("POWER", SMALL, DIM, left, 310)
    pygame.draw.rect(screen, (29, 40, 67), (left, 337, 150, 9), border_radius=5)
    if game["power"] > 0:
        pygame.draw.rect(screen, CYAN, (left, 337, int(150 * game["power"] / 8), 9), border_radius=5)
    text("MOVE", SMALL, DIM, left, 379)
    text("Arrows / WASD", FONT, WHITE, left, 403)
    text("P  pause", SMALL, DIM, left, 447)
    text("R  restart", SMALL, DIM, left, 472)
    text("Collect every dot!", SMALL, DIM, left, 533)


def draw_overlay(title, subtitle, color=YELLOW):
    veil = pygame.Surface((COLS * TILE, ROWS * TILE), pygame.SRCALPHA)
    veil.fill((4, 8, 24, 190))
    screen.blit(veil, (0, 0))
    title_image = BIG.render(title, True, color)
    subtitle_image = FONT.render(subtitle, True, WHITE)
    screen.blit(title_image, title_image.get_rect(center=(COLS * TILE // 2, ROWS * TILE // 2 - 24)))
    screen.blit(subtitle_image, subtitle_image.get_rect(center=(COLS * TILE // 2, ROWS * TILE // 2 + 29)))


def draw():
    draw_maze()
    for ghost in game["ghosts"]:
        draw_ghost(ghost)
    draw_player()
    draw_hud()
    if not game["started"]:
        draw_overlay("PAC-MAN", "Press any direction to start", CYAN)
    elif game["paused"]:
        draw_overlay("PAUSED", "Press P to continue", CYAN)
    elif game["over"]:
        draw_overlay("GAME OVER", "Press R to play again", PINK)
    elif game["won"]:
        draw_overlay("YOU WIN!", "Press R for another round", GREEN)
    pygame.display.flip()


running = True
while running:
    dt = min(clock.tick(60) / 1000.0, 0.05)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r:
                game = new_game()
            elif event.key == pygame.K_p and game["started"] and not game["over"] and not game["won"]:
                game["paused"] = not game["paused"]
            elif event.key in KEY_DIRS:
                game["queued"] = KEY_DIRS[event.key]
                game["started"] = True
    update(dt)
    draw()

pygame.quit()