"""Pac-Man-inspired arcade game. Install pygame: python -m pip install pygame"""

import math
import random
from array import array

import pygame

TILE, COLS, ROWS = 30, 21, 21
HUD = 76
WIDTH, HEIGHT = COLS * TILE, ROWS * TILE + HUD
NAVY, YELLOW = (5, 8, 27), (255, 221, 36)
KEYS = {
	pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
	pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
	pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
	pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
}


def tone(frequency, duration=0.1):
	"""Create a short synthesized sound without needing audio files."""
	rate = 22050
	samples = array("h")
	for i in range(int(rate * duration)):
		fade = 1 - i / (rate * duration)
		samples.append(int(32767 * 0.18 * fade * math.sin(2 * math.pi * frequency * i / rate)))
	return pygame.mixer.Sound(buffer=samples.tobytes())


def build_maze():
	walls = [[x in (0, COLS - 1) or y in (0, ROWS - 1)
			  for x in range(COLS)] for y in range(ROWS)]
	for y in (5, 10, 15):
		for x in range(1, COLS - 1):
			if x not in (2, 6, 10, 14, 18):
				walls[y][x] = True
	for x in (5, 10, 15):
		for y in range(1, ROWS - 1):
			if y not in (2, 6, 10, 14, 18):
				walls[y][x] = True
	return walls


class Ghost:
	COLORS = ((255, 63, 91), (255, 130, 211), (65, 225, 255), (255, 167, 54))

	def __init__(self, home, index):
		self.x, self.y = home
		self.home, self.index = home, index
		self.color, self.direction = self.COLORS[index], (0, 0)


class Game:
	def __init__(self):
		pygame.init()
		self.sounds = {}
		try:
			pygame.mixer.init(frequency=22050, size=-16, channels=1)
			self.sounds = {"dot": tone(720, 0.045), "power": tone(390, 0.25),
						   "eat": tone(980, 0.18), "start": tone(520, 0.3)}
		except pygame.error:
			pass  # Audio is optional; the game still works without a sound device.
		pygame.display.set_caption("PAC-MAN | Neon Maze")
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.font = pygame.font.SysFont("Arial", 21, bold=True)
		self.small = pygame.font.SysFont("Arial", 14, bold=True)
		self.large = pygame.font.SysFont("Arial", 44, bold=True)
		self.walls = build_maze()
		self.reset()

	def reset(self):
		self.pac = [1, 1]
		self.direction = self.queued = (0, 0)
		self.score, self.lives, self.power = 0, 3, 0.0
		self.dots = {(x, y) for y in range(1, ROWS - 1) for x in range(1, COLS - 1)
					 if not self.walls[y][x] and (x, y) != (1, 1)}
		self.power_dots = {(2, 2), (18, 2), (2, 18), (18, 18)}
		self.dots -= self.power_dots
		homes = ((19, 1), (19, 19), (1, 19), (10, 19))
		self.ghosts = [Ghost(home, i) for i, home in enumerate(homes)]
		self.move_timer = self.ghost_timer = self.animation = self.elapsed = 0.0
		self.state, self.paused = "ready", False

	def sound(self, name):
		if name in self.sounds:
			self.sounds[name].play()

	def open_cell(self, x, y):
		return 0 <= x < COLS and 0 <= y < ROWS and not self.walls[y][x]

	def neighbors(self, pos):
		x, y = pos
		return [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
				if self.open_cell(x + dx, y + dy)]

	def player_step(self):
		x, y = self.pac
		dx, dy = self.queued
		if self.open_cell(x + dx, y + dy):
			self.direction = self.queued
		dx, dy = self.direction
		if self.open_cell(x + dx, y + dy):
			self.pac[0] += dx
			self.pac[1] += dy
		pos = tuple(self.pac)
		if pos in self.dots:
			self.dots.remove(pos)
			self.score += 10
			self.sound("dot")
		if pos in self.power_dots:
			self.power_dots.remove(pos)
			self.score += 50
			self.power = 8.0
			self.sound("power")
		if not self.dots and not self.power_dots:
			self.state = "won"

	def ghost_step(self, ghost):
		target = tuple(self.pac)
		if ghost.index == 1:
			target = (max(1, min(COLS - 2, target[0] + self.direction[0] * 3)),
					  max(1, min(ROWS - 2, target[1] + self.direction[1] * 3)))
		elif ghost.index == 2:
			target = (COLS - 1 - target[0], ROWS - 1 - target[1])
		elif ghost.index == 3 and abs(ghost.x - target[0]) + abs(ghost.y - target[1]) < 7:
			target = ghost.home
		# Breadth-first search gives ghosts a valid route through the corridors.
		distances, queue = {target: 0}, [target]
		for cell in queue:
			for nxt in self.neighbors(cell):
				if nxt not in distances:
					distances[nxt] = distances[cell] + 1
					queue.append(nxt)
		options = self.neighbors((ghost.x, ghost.y))
		if options:
			measure = max if self.power > 0 else min
			best = measure(distances.get(pos, 999) for pos in options)
			ghost.x, ghost.y = random.choice([p for p in options if distances.get(p, 999) == best])

	def check_collisions(self):
		for ghost in self.ghosts:
			if (ghost.x, ghost.y) != tuple(self.pac):
				continue
			if self.power > 0:
				ghost.x, ghost.y = ghost.home
				self.score += 200
				self.sound("eat")
			else:
				self.lives -= 1
				if self.lives <= 0:
					self.state = "over"
				else:
					self.pac = [1, 1]
					self.direction = self.queued = (0, 0)
					for other in self.ghosts:
						other.x, other.y = other.home
					self.power = 1.2
				break

	def update(self, dt):
		if self.state != "playing" or self.paused:
			return
		self.elapsed += dt
		self.animation += dt * 13
		self.power = max(0.0, self.power - dt)
		self.move_timer += dt
		if self.move_timer >= 0.115:
			self.move_timer %= 0.115
			self.player_step()
		self.ghost_timer += dt
		if self.ghost_timer >= (0.31 if self.power else 0.22):
			self.ghost_timer = 0
			for ghost in self.ghosts:
				self.ghost_step(ghost)
		self.check_collisions()

	def draw_maze(self):
		self.screen.fill(NAVY)
		for y in range(ROWS):
			for x in range(COLS):
				rect = pygame.Rect(x * TILE, y * TILE, TILE, TILE)
				if self.walls[y][x]:
					pygame.draw.rect(self.screen, (12, 34, 112), rect.inflate(-2, -2), border_radius=7)
					pygame.draw.rect(self.screen, (44, 145, 255), rect.inflate(-5, -5), 2, border_radius=6)
				else:
					pygame.draw.rect(self.screen, (7, 10, 30), rect)
		for x, y in self.dots:
			pygame.draw.circle(self.screen, (255, 220, 179), (x * TILE + 15, y * TILE + 15), 2)
		radius = 6 + int(2 * math.sin(self.elapsed * 7))
		for x, y in self.power_dots:
			center = (x * TILE + 15, y * TILE + 15)
			pygame.draw.circle(self.screen, (255, 200, 70), center, radius + 4, 1)
			pygame.draw.circle(self.screen, (255, 238, 168), center, radius)

	def draw_pacman(self):
		x, y = self.pac
		cx, cy = x * TILE + 15, y * TILE + 15
		pygame.draw.circle(self.screen, YELLOW, (cx, cy), 12)
		if self.direction != (0, 0):
			angle = math.atan2(self.direction[1], self.direction[0])
			spread = abs(math.sin(self.animation)) * 0.48
			points = [(cx, cy)] + [(cx + math.cos(a) * 14, cy + math.sin(a) * 14)
									for a in (angle - spread + 2 * spread * i / 12 for i in range(13))]
			pygame.draw.polygon(self.screen, NAVY, points)

	def draw_ghost(self, ghost):
		cx, cy = ghost.x * TILE + 15, ghost.y * TILE + 15
		color = (64, 91, 255) if self.power else ghost.color
		pygame.draw.circle(self.screen, color, (cx, cy - 2), 12)
		pygame.draw.rect(self.screen, color, (cx - 12, cy - 2, 24, 12))
		for ox in (-8, 0, 8):
			pygame.draw.circle(self.screen, color, (cx + ox, cy + 9), 4)
		for ox in (-5, 5):
			pygame.draw.ellipse(self.screen, (255, 255, 255), (cx + ox - 3, cy - 7, 7, 9))
			pygame.draw.circle(self.screen, (20, 35, 95), (cx + ox + ghost.direction[0],
														  cy - 3 + ghost.direction[1]), 2)

	def draw(self):
		self.draw_maze()
		for ghost in self.ghosts:
			self.draw_ghost(ghost)
		self.draw_pacman()
		top = ROWS * TILE
		pygame.draw.rect(self.screen, (9, 13, 39), (0, top, WIDTH, HUD))
		pygame.draw.line(self.screen, (40, 67, 148), (20, top + 2), (WIDTH - 20, top + 2), 2)
		self.screen.blit(self.font.render("PAC-MAN", True, YELLOW), (22, top + 12))
		self.screen.blit(self.small.render(f"SCORE  {self.score:06d}", True, (227, 238, 255)), (22, top + 44))
		for i in range(self.lives):
			cx = WIDTH - 34 - i * 30
			pygame.draw.circle(self.screen, YELLOW, (cx, top + 24), 10)
		hint = "ARROWS / WASD  •  P: PAUSE  •  ENTER: RESTART"
		self.screen.blit(self.small.render(hint, True, (151, 174, 222)),
						 (WIDTH - self.small.size(hint)[0] - 22, top + 49))
		overlay = {"ready": ("PAC-MAN", "PRESS ENTER OR AN ARROW KEY TO START"),
				   "won": ("YOU WIN!", f"SCORE {self.score}  •  PRESS ENTER TO PLAY AGAIN"),
				   "over": ("GAME OVER", f"SCORE {self.score}  •  PRESS ENTER TO RETRY")}.get(self.state)
		if self.paused:
			overlay = ("PAUSED", "PRESS P TO CONTINUE")
		if overlay:
			veil = pygame.Surface((WIDTH, ROWS * TILE), pygame.SRCALPHA)
			veil.fill((2, 4, 20, 190))
			self.screen.blit(veil, (0, 0))
			title = self.large.render(overlay[0], True, YELLOW)
			prompt = self.font.render(overlay[1], True, (225, 239, 255))
			self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15)))
			self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
		pygame.display.flip()

	def run(self):
		running = True
		while running:
			dt = min(self.clock.tick(60) / 1000.0, 0.05)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						running = False
					elif event.key == pygame.K_p and self.state == "playing":
						self.paused = not self.paused
					elif event.key == pygame.K_RETURN and self.state in ("ready", "won", "over"):
						if self.state != "ready":
							self.reset()
						self.state = "playing"
						self.sound("start")
					elif event.key in KEYS:
						self.queued = KEYS[event.key]
						if self.state == "ready":
							self.state = "playing"
							self.sound("start")
			self.update(dt)
			self.draw()
		pygame.quit()


if __name__ == "__main__":
	Game().run()
