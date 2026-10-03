import pygame
import math
import random
import array

# ==========================================
# 1. AUDIO ENGINE (Procedural Retro Synth)
# ==========================================
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.font.init()

def generate_sound(freq_start, freq_end, duration_s, wave_type="sine", volume=0.25):
    """Generates an 8-bit style retro sound wave without external assets."""
    sample_rate = 44100
    n_samples = int(sample_rate * duration_s)
    buf = array.array('h')
    
    for i in range(n_samples):
        t = i / sample_rate
        frac = i / n_samples
        freq = freq_start + (freq_end - freq_start) * frac
        phase = 2.0 * math.pi * freq * t
        
        if wave_type == "sine":
            val = math.sin(phase)
        elif wave_type == "square":
            val = 1.0 if math.sin(phase) >= 0 else -1.0
        elif wave_type == "noise":
            val = random.uniform(-1.0, 1.0)
        else:
            val = 0.0

        # ADSR Envelope (Attack - Linear Decay)
        amp = (1.0 - frac) * volume
        sample = int(val * amp * 32767)
        buf.append(max(-32768, min(32767, sample)))
        
    return pygame.mixer.Sound(buffer=buf)

# Audio SFX library
SND_CHOMP_A = generate_sound(450, 220, 0.08, "square", 0.15)
SND_CHOMP_B = generate_sound(260, 520, 0.08, "square", 0.15)
SND_POWER   = generate_sound(180, 750, 0.45, "sine", 0.3)
SND_EAT_GHOST = generate_sound(800, 140, 0.35, "square", 0.35)
SND_DEATH   = generate_sound(600, 80, 0.9, "noise", 0.4)
SND_WIN     = generate_sound(300, 950, 0.6, "sine", 0.3)

# ==========================================
# 2. CONFIGURATION & MAZE LAYOUT
# ==========================================
TILE_SIZE = 26
GRID_COLS = 21
GRID_ROWS = 21
SCREEN_WIDTH = GRID_COLS * TILE_SIZE
SCREEN_HEIGHT = GRID_ROWS * TILE_SIZE + 60  # Extra bar for score & UI

# Palette
CLR_BG = (10, 10, 16)
CLR_WALL = (24, 48, 192)
CLR_WALL_INSET = (60, 100, 255)
CLR_PELLET = (255, 200, 180)
CLR_POWER = (255, 230, 90)
CLR_PACMAN = (255, 225, 0)
CLR_EYE = (245, 245, 255)
CLR_PUPIL = (15, 25, 120)
CLR_FRIGHTENED = (40, 70, 240)
CLR_FLASH = (240, 240, 255)

# Maze Map: 
# 1 = Wall, 0 = Pellet, 2 = Power Pellet, 3 = Empty/Ghost Base, 4 = Gate
RAW_MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,2,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,3,1,3,1,1,1,0,1,1,1,1,1],
    [3,3,3,3,1,0,1,3,3,3,3,3,3,3,1,0,1,3,3,3,3],
    [1,1,1,1,1,0,1,3,1,1,4,1,1,3,1,0,1,1,1,1,1],
    [3,3,3,3,3,0,3,3,1,3,3,3,1,3,3,0,3,3,3,3,3],
    [1,1,1,1,1,0,1,3,1,1,1,1,1,3,1,0,1,1,1,1,1],
    [3,3,3,3,1,0,1,3,3,3,3,3,3,3,1,0,1,3,3,3,3],
    [1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1],
    [1,2,0,0,1,0,0,0,0,0,3,0,0,0,0,0,1,0,0,2,1],
    [1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1],
    [1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# ==========================================
# 3. GAME OBJECTS
# ==========================================
class Pacman:
    def __init__(self, col, row):
        self.init_col = col
        self.init_row = row
        self.reset()
        
    def reset(self):
        self.x = self.init_col * TILE_SIZE + TILE_SIZE // 2
        self.y = self.init_row * TILE_SIZE + TILE_SIZE // 2
        self.speed = 2.4
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.mouth_angle = 45
        self.mouth_dir = -2.5
        self.angle = 0
        self.alive = True
        self.death_timer = 0
        
    def update(self, maze):
        if not self.alive:
            self.death_timer += 1
            return

        # Animate mouth chomp
        self.mouth_angle += self.mouth_dir
        if self.mouth_angle <= 4 or self.mouth_angle >= 48:
            self.mouth_dir *= -1

        # Check turn at center of tile
        tile_center_x = (int(self.x // TILE_SIZE)) * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = (int(self.y // TILE_SIZE)) * TILE_SIZE + TILE_SIZE // 2

        if abs(self.x - tile_center_x) <= self.speed and abs(self.y - tile_center_y) <= self.speed:
            cur_c = int(self.x // TILE_SIZE)
            cur_r = int(self.y // TILE_SIZE)
            
            # Attempt requested direction
            if self.next_dx != 0 or self.next_dy != 0:
                target_c = (cur_c + self.next_dx) % GRID_COLS
                target_r = (cur_r + self.next_dy) % GRID_ROWS
                if maze[target_r][target_c] not in (1, 4):
                    self.dx = self.next_dx
                    self.dy = self.next_dy
                    self.x = tile_center_x
                    self.y = tile_center_y

            # Check if current direction is blocked
            ahead_c = (cur_c + self.dx) % GRID_COLS
            ahead_r = (cur_r + self.dy) % GRID_ROWS
            if maze[ahead_r][ahead_c] in (1, 4):
                self.dx = 0
                self.dy = 0
                self.x = tile_center_x
                self.y = tile_center_y

        self.x = (self.x + self.dx * self.speed) % (GRID_COLS * TILE_SIZE)
        self.y = (self.y + self.dy * self.speed) % (GRID_ROWS * TILE_SIZE)

        # Facing rotation angle
        if self.dx > 0: self.angle = 0
        elif self.dx < 0: self.angle = 180
        elif self.dy > 0: self.angle = 270
        elif self.dy < 0: self.angle = 90

    def draw(self, surface):
        px, py = int(self.x), int(self.y)
        radius = TILE_SIZE // 2 - 2

        if not self.alive:
            # Dying spin animation
            anim_prog = min(1.0, self.death_timer / 60.0)
            end_angle = 360 * (1.0 - anim_prog)
            if end_angle > 0:
                pygame.draw.arc(surface, CLR_PACMAN, (px - radius, py - radius, radius * 2, radius * 2), 0, math.radians(end_angle), radius)
            return

        # Smooth polygon pie for mouth opening
        start_rad = math.radians(self.angle + self.mouth_angle)
        end_rad = math.radians(self.angle + 360 - self.mouth_angle)
        points = [(px, py)]
        steps = 24
        for s in range(steps + 1):
            theta = start_rad + (end_rad - start_rad) * (s / steps)
            points.append((px + radius * math.cos(theta), py - radius * math.sin(theta)))
            
        pygame.draw.polygon(surface, CLR_PACMAN, points)


class Ghost:
    def __init__(self, col, row, color, name):
        self.init_col = col
        self.init_row = row
        self.color = color
        self.name = name
        self.reset()

    def reset(self):
        self.x = self.init_col * TILE_SIZE + TILE_SIZE // 2
        self.y = self.init_row * TILE_SIZE + TILE_SIZE // 2
        self.dx = 0
        self.dy = -1
        self.speed = 2.0
        self.frightened = False
        self.frightened_timer = 0
        self.eaten = False

    def update(self, maze, pac_x, pac_y):
        tile_center_x = (int(self.x // TILE_SIZE)) * TILE_SIZE + TILE_SIZE // 2
        tile_center_y = (int(self.y // TILE_SIZE)) * TILE_SIZE + TILE_SIZE // 2

        if abs(self.x - tile_center_x) <= self.speed and abs(self.y - tile_center_y) <= self.speed:
            self.x = tile_center_x
            self.y = tile_center_y
            cur_c = int(self.x // TILE_SIZE)
            cur_r = int(self.y // TILE_SIZE)

            # Available legal moves (avoid reversing 180 degrees)
            valid_dirs = []
            for d_col, d_row in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                if (d_col, d_row) == (-self.dx, -self.dy):
                    continue
                next_c = (cur_c + d_col) % GRID_COLS
                next_r = (cur_r + d_row) % GRID_ROWS
                # Normal ghosts avoid walls and gate
                tile_val = maze[next_r][next_c]
                if tile_val != 1 and (self.eaten or tile_val != 4):
                    valid_dirs.append((d_col, d_row))

            if not valid_dirs:
                valid_dirs.append((-self.dx, -self.dy))

            # Direction decision logic
            if self.eaten:
                # Return straight to home base center
                target_x, target_y = 10 * TILE_SIZE, 9 * TILE_SIZE
                valid_dirs.sort(key=lambda d: math.hypot((cur_c + d[0]) * TILE_SIZE - target_x, (cur_r + d[1]) * TILE_SIZE - target_y))
                self.dx, self.dy = valid_dirs[0]
                if abs(self.x - target_x) < TILE_SIZE and abs(self.y - target_y) < TILE_SIZE:
                    self.eaten = False
            elif self.frightened:
                # Random evasion
                self.dx, self.dy = random.choice(valid_dirs)
            else:
                # Target Pac-Man with simple tracking heuristic
                valid_dirs.sort(key=lambda d: math.hypot((cur_c + d[0]) * TILE_SIZE - pac_x, (cur_r + d[1]) * TILE_SIZE - pac_y))
                self.dx, self.dy = valid_dirs[0]

        # Velocity & speed tuning
        cur_spd = 1.3 if self.frightened else (3.6 if self.eaten else self.speed)
        self.x = (self.x + self.dx * cur_spd) % (GRID_COLS * TILE_SIZE)
        self.y = (self.y + self.dy * cur_spd) % (GRID_ROWS * TILE_SIZE)

        # Fright timer tick
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False

    def draw(self, surface, tick):
        px, py = int(self.x), int(self.y)
        r = TILE_SIZE // 2 - 2

        # 1. Body Rendering
        if not self.eaten:
            if self.frightened:
                # Flash near the end of frightened state
                ghost_col = CLR_FLASH if (self.frightened_timer < 100 and (tick // 8) % 2 == 0) else CLR_FRIGHTENED
            else:
                ghost_col = self.color

            # Head hemisphere
            pygame.draw.circle(surface, ghost_col, (px, py - 2), r)
            # Body skirt
            pygame.draw.rect(surface, ghost_col, (px - r, py - 2, r * 2, r + 2))
            
            # Wavy skirt tentacles
            tentacle_w = (r * 2) / 3
            wave_offset = 2 if (tick // 10) % 2 == 0 else 0
            for i in range(3):
                tx = px - r + i * tentacle_w + tentacle_w / 2
                pygame.draw.circle(surface, ghost_col, (int(tx), int(py + r - wave_offset)), int(tentacle_w / 2))

        # 2. Eye & Pupil Rendering
        eye_offset_x = self.dx * 3
        eye_offset_y = self.dy * 3
        for side in (-4, 4):
            ex = px + side
            ey = py - 4
            # White sclera
            pygame.draw.ellipse(surface, CLR_EYE, (ex - 3, ey - 5, 7, 9))
            # Pupil tracking look direction
            pygame.draw.circle(surface, CLR_PUPIL, (ex + eye_offset_x, ey + eye_offset_y), 2)

# ==========================================
# 4. GAME STATE ENGINE
# ==========================================
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man Classic Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Courier New", 18, bold=True)
        self.large_font = pygame.font.SysFont("Courier New", 28, bold=True)
        
        self.maze = [row[:] for row in RAW_MAZE]
        self.pacman = Pacman(10, 16)
        self.ghosts = [
            Ghost(9, 9, (255, 0, 40), "Blinky"),
            Ghost(10, 9, (255, 185, 255), "Pinky"),
            Ghost(11, 9, (0, 235, 255), "Inky"),
            Ghost(10, 8, (255, 185, 80), "Clyde")
        ]
        self.score = 0
        self.lives = 3
        self.chomp_alt = False
        self.total_pellets = sum(row.count(0) + row.count(2) for row in self.maze)
        self.pellets_eaten = 0
        self.game_over = False
        self.won = False
        self.particles = []

    def add_sparkles(self, x, y, color):
        for _ in range(8):
            self.particles.append([x, y, random.uniform(-2, 2), random.uniform(-2, 2), random.randint(10, 20), color])

    def reset_round(self):
        self.pacman.reset()
        for g in self.ghosts:
            g.reset()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_over or self.won:
                    if event.key == pygame.K_r:
                        self.__init__()
                    return True
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.pacman.next_dx, self.pacman.next_dy = 0, -1
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.pacman.next_dx, self.pacman.next_dy = 0, 1
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    self.pacman.next_dx, self.pacman.next_dy = -1, 0
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    self.pacman.next_dx, self.pacman.next_dy = 1, 0
        return True

    def update(self):
        if self.game_over or self.won:
            return

        self.pacman.update(self.maze)

        if not self.pacman.alive:
            if self.pacman.death_timer > 60:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
                else:
                    self.reset_round()
            return

        # Pellet collision
        c = int(self.pacman.x // TILE_SIZE)
        r = int(self.pacman.y // TILE_SIZE)
        
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
            if self.maze[r][c] == 0:  # Normal pellet
                self.maze[r][c] = 3
                self.score += 10
                self.pellets_eaten += 1
                self.chomp_alt = not self.chomp_alt
                (SND_CHOMP_A if self.chomp_alt else SND_CHOMP_B).play()
            elif self.maze[r][c] == 2:  # Power pellet
                self.maze[r][c] = 3
                self.score += 50
                self.pellets_eaten += 1
                SND_POWER.play()
                self.add_sparkles(c * TILE_SIZE + 13, r * TILE_SIZE + 13, CLR_POWER)
                for g in self.ghosts:
                    g.frightened = True
                    g.frightened_timer = 400

        # Check win condition
        if self.pellets_eaten >= self.total_pellets:
            self.won = True
            SND_WIN.play()

        # Ghost logic & collisions
        for g in self.ghosts:
            g.update(self.maze, self.pacman.x, self.pacman.y)
            dist = math.hypot(self.pacman.x - g.x, self.pacman.y - g.y)
            if dist < TILE_SIZE * 0.7:
                if g.frightened and not g.eaten:
                    g.eaten = True
                    g.frightened = False
                    self.score += 200
                    SND_EAT_GHOST.play()
                    self.add_sparkles(g.x, g.y, (120, 180, 255))
                elif not g.eaten:
                    self.pacman.alive = False
                    SND_DEATH.play()

        # Update sparkles
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] <= 0:
                self.particles.remove(p)

    def draw(self, tick):
        self.screen.fill(CLR_BG)

        # 1. Draw Maze & Pellets
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                tile = self.maze[r][c]
                rx, ry = c * TILE_SIZE, r * TILE_SIZE
                
                if tile == 1:
                    # Neon dual-border aesthetic for labyrinth walls
                    pygame.draw.rect(self.screen, CLR_WALL, (rx, ry, TILE_SIZE, TILE_SIZE), border_radius=4)
                    pygame.draw.rect(self.screen, CLR_WALL_INSET, (rx + 2, ry + 2, TILE_SIZE - 4, TILE_SIZE - 4), width=1, border_radius=3)
                elif tile == 4:
                    # Ghost house barrier gate
                    pygame.draw.line(self.screen, (255, 180, 200), (rx, ry + TILE_SIZE // 2), (rx + TILE_SIZE, ry + TILE_SIZE // 2), 3)
                elif tile == 0:
                    # Regular dot
                    pygame.draw.circle(self.screen, CLR_PELLET, (rx + TILE_SIZE // 2, ry + TILE_SIZE // 2), 2)
                elif tile == 2:
                    # Pulsing power pellet
                    pulse = abs(math.sin(tick * 0.08)) * 2.5
                    pygame.draw.circle(self.screen, CLR_POWER, (rx + TILE_SIZE // 2, ry + TILE_SIZE // 2), int(4 + pulse))

        # 2. Draw Particles
        for p in self.particles:
            pygame.draw.circle(self.screen, p[5], (int(p[0]), int(p[1])), max(1, p[4] // 4))

        # 3. Draw Pac-Man & Ghosts
        self.pacman.draw(self.screen)
        for g in self.ghosts:
            g.draw(self.screen, tick)

        # 4. HUD / UI Bar
        hud_top = GRID_ROWS * TILE_SIZE
        pygame.draw.rect(self.screen, (15, 15, 25), (0, hud_top, SCREEN_WIDTH, 60))
        pygame.draw.line(self.screen, (40, 50, 100), (0, hud_top), (SCREEN_WIDTH, hud_top), 2)
        
        score_surf = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (16, hud_top + 18))

        # Lives Indicator icons
        for l in range(self.lives):
            lx = SCREEN_WIDTH - 24 - (l * 22)
            ly = hud_top + 28
            pygame.draw.circle(self.screen, CLR_PACMAN, (lx, ly), 8)

        # End Condition Overlays
        if self.game_over:
            box = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            box.fill((0, 0, 0, 180))
            self.screen.blit(box, (0, 0))
            msg = self.large_font.render("GAME OVER", True, (255, 50, 50))
            sub = self.font.render("Press 'R' to Restart", True, (200, 200, 200))
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        if self.won:
            box = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            box.fill((0, 0, 0, 180))
            self.screen.blit(box, (0, 0))
            msg = self.large_font.render("YOU WIN!", True, (50, 255, 100))
            sub = self.font.render("Press 'R' to Play Again", True, (200, 200, 200))
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.flip()

    def run(self):
        tick = 0
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw(tick)
            self.clock.tick(60)
            tick += 1
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()