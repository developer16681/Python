import math
import random
import sys

import pygame

WINDOW_W, WINDOW_H = 1280, 720
FOV = math.radians(72)
MAX_DEPTH = 24.0
MOVE_SPEED = 2.7
TURN_SPEED = 2.4
PLAYER_RADIUS = 0.22

MAP = [
    "111111111111111",
    "100000000000001",
    "101111011111101",
    "100001000001001",
    "101101011101101",
    "100100000001001",
    "101101110101101",
    "100000010001001",
    "111011110101111",
    "100010000001001",
    "101110111101101",
    "100000100000001",
    "101111101111101",
    "100000000000001",
    "111111111111111",
]


class Enemy:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.hp = 2
        self.speed = 0.8
        self.damage = 12

    @property
    def alive(self):
        return self.hp > 0


class Player:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.angle = 0.0
        self.health = 100.0
        self.fire_cooldown = 0.0
        self.kills = 0


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Nightfall: Siege")
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.big_font = pygame.font.SysFont("arial", 52)
        self.small_font = pygame.font.SysFont("arial", 18)
        self.player = Player(2.5, 2.5)
        self.enemies = [
            Enemy(6.5, 2.8),
            Enemy(11.0, 4.4),
            Enemy(9.0, 11.2),
            Enemy(4.5, 10.0),
            Enemy(12.2, 11.5),
        ]
        self.game_over = False
        self.flash = 0.0
        self.crosshair_color = (255, 255, 255)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        pygame.mouse.set_pos((WINDOW_W // 2, WINDOW_H // 2))

    def map_size(self):
        return len(MAP[0]), len(MAP)

    def is_wall(self, x, y):
        if x < 0 or y < 0:
            return True
        tile_x = int(x)
        tile_y = int(y)
        if tile_y < 0 or tile_y >= len(MAP):
            return True
        if tile_x < 0 or tile_x >= len(MAP[tile_y]):
            return True
        return MAP[tile_y][tile_x] == "1"

    def cast_ray(self, angle, max_depth=MAX_DEPTH):
        distance = 0.0
        while distance < max_depth:
            test_x = self.player.x + math.cos(angle) * distance
            test_y = self.player.y + math.sin(angle) * distance
            if self.is_wall(test_x, test_y):
                return distance, int(test_x), int(test_y)
            distance += 0.04
        return max_depth, -1, -1

    def shoot(self):
        if self.game_over:
            return
        best_target = None
        best_dist = 9999.0
        best_angle = 0.0
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.hypot(dx, dy)
            target_angle = math.atan2(dy, dx) - self.player.angle
            target_angle = (target_angle + math.pi) % (2 * math.pi) - math.pi
            if abs(target_angle) > 0.18:
                continue
            if dist < best_dist:
                best_dist = dist
                best_target = enemy
                best_angle = target_angle
        if best_target is not None:
            best_target.hp -= 1
            self.flash = 0.14
            if best_target.hp <= 0:
                self.player.kills += 1
                best_target.hp = 0

    def move_player(self, dt):
        keys = pygame.key.get_pressed()
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_w]:
            dx += math.cos(self.player.angle) * MOVE_SPEED * dt
            dy += math.sin(self.player.angle) * MOVE_SPEED * dt
        if keys[pygame.K_s]:
            dx -= math.cos(self.player.angle) * MOVE_SPEED * dt
            dy -= math.sin(self.player.angle) * MOVE_SPEED * dt
        if keys[pygame.K_a]:
            dx += math.cos(self.player.angle - math.pi / 2) * MOVE_SPEED * dt
            dy += math.sin(self.player.angle - math.pi / 2) * MOVE_SPEED * dt
        if keys[pygame.K_d]:
            dx += math.cos(self.player.angle + math.pi / 2) * MOVE_SPEED * dt
            dy += math.sin(self.player.angle + math.pi / 2) * MOVE_SPEED * dt

        if dx != 0.0 or dy != 0.0:
            next_x = self.player.x + dx
            next_y = self.player.y + dy
            if not self.is_wall(next_x, self.player.y):
                self.player.x = next_x
            if not self.is_wall(self.player.x, next_y):
                self.player.y = next_y

        if keys[pygame.K_LEFT]:
            self.player.angle -= TURN_SPEED * dt
        if keys[pygame.K_RIGHT]:
            self.player.angle += TURN_SPEED * dt

        self.player.angle %= 2 * math.pi

    def update_enemies(self, dt):
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx = self.player.x - enemy.x
            dy = self.player.y - enemy.y
            dist = math.hypot(dx, dy)
            if dist < 0.1:
                dist = 0.1
            if dist < 1.8:
                move_x = (dx / dist) * enemy.speed * dt
                move_y = (dy / dist) * enemy.speed * dt
                nx = enemy.x + move_x
                ny = enemy.y + move_y
                if not self.is_wall(nx, enemy.y):
                    enemy.x = nx
                if not self.is_wall(enemy.x, ny):
                    enemy.y = ny
            if dist < 0.7:
                self.player.health -= enemy.damage * dt
                self.player.health = max(0.0, self.player.health)
        if self.player.health <= 0:
            self.game_over = True

    def draw_background(self):
        for y in range(WINDOW_H // 2):
            shade = 30 + (y / (WINDOW_H // 2)) * 150
            color = (int(shade), int(shade + 15), int(shade + 30))
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_W, y))

        for y in range(WINDOW_H // 2, WINDOW_H):
            shade = 18 + ((y - WINDOW_H // 2) / (WINDOW_H // 2)) * 110
            color = (int(shade), int(shade), int(shade + 8))
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_W, y))

    def draw_scene(self):
        self.draw_background()

        for column in range(0, WINDOW_W, 2):
            ray_angle = self.player.angle - FOV / 2 + (column / WINDOW_W) * FOV
            dist, wall_x, wall_y = self.cast_ray(ray_angle)
            corrected = dist * math.cos(ray_angle - self.player.angle)
            corrected = max(corrected, 0.01)
            wall_height = (WINDOW_H / corrected) * 0.8
            top = WINDOW_H / 2 - wall_height / 2
            bottom = WINDOW_H / 2 + wall_height / 2
            shade = max(25, 255 - dist * 18)
            wall_color = (int(shade * 0.45), int(shade * 0.7), int(shade * 0.9))
            if wall_x != -1 and wall_y != -1:
                variation = ((wall_x * 31 + wall_y * 17) % 25)
                wall_color = (
                    int(max(30, shade - variation * 1.2)),
                    int(max(25, shade * 0.8 - variation)),
                    int(max(20, shade * 0.6 - variation * 0.5)),
                )
            pygame.draw.rect(self.screen, wall_color, (column, top, 2, max(4, bottom - top)))

    def draw_enemies(self):
        sprites = []
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx = enemy.x - self.player.x
            dy = enemy.y - self.player.y
            dist = math.hypot(dx, dy)
            if dist <= 0.001:
                continue
            rel_angle = math.atan2(dy, dx) - self.player.angle
            rel_angle = (rel_angle + math.pi) % (2 * math.pi) - math.pi
            if abs(rel_angle) > FOV * 0.7:
                continue
            wall_dist, _, _ = self.cast_ray(self.player.angle + rel_angle)
            if wall_dist < dist:
                continue
            sprites.append((dist, rel_angle, enemy))

        sprites.sort(key=lambda item: item[0], reverse=True)
        for dist, rel_angle, enemy in sprites:
            size = (WINDOW_H / max(dist, 0.2)) * 0.42
            x = WINDOW_W / 2 + math.tan(rel_angle) * (WINDOW_W / 2) / math.tan(FOV / 2)
            y = WINDOW_H * 0.76
            body = pygame.Rect(x - size / 2, y - size * 0.9, size, size * 1.1)
            shade = max(40, 255 - dist * 18)
            color = (shade // 3, shade, shade // 2)
            pygame.draw.rect(self.screen, color, body)
            head = pygame.Rect(body.centerx - size * 0.2, body.y + size * 0.05, size * 0.4, size * 0.4)
            pygame.draw.rect(self.screen, (200, 200, 200), head)
            eye = pygame.Rect(head.centerx - size * 0.08, head.y + size * 0.08, size * 0.12, size * 0.12)
            pygame.draw.rect(self.screen, (40, 40, 40), eye)

    def draw_hud(self):
        # Vignette
        vignette = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
        for y in range(WINDOW_H):
            alpha = int(min(130, (min(y, WINDOW_H - y) / (WINDOW_H / 2)) * 110))
            pygame.draw.line(vignette, (0, 0, 0, alpha), (0, y), (WINDOW_W, y))
        self.screen.blit(vignette, (0, 0))

        # Crosshair
        cx, cy = WINDOW_W // 2, WINDOW_H // 2
        pygame.draw.line(self.screen, self.crosshair_color, (cx - 12, cy), (cx - 4, cy), 2)
        pygame.draw.line(self.screen, self.crosshair_color, (cx + 4, cy), (cx + 12, cy), 2)
        pygame.draw.line(self.screen, self.crosshair_color, (cx, cy - 12), (cx, cy - 4), 2)
        pygame.draw.line(self.screen, self.crosshair_color, (cx, cy + 4), (cx, cy + 12), 2)

        # Health bar
        bar_w = 260
        bar_h = 18
        health_w = (self.player.health / 100.0) * bar_w
        pygame.draw.rect(self.screen, (45, 45, 45), (24, 24, bar_w, bar_h), border_radius=9)
        pygame.draw.rect(self.screen, (210, 70, 70), (24, 24, health_w, bar_h), border_radius=9)
        self.screen.blit(self.font.render(f"Health: {int(self.player.health)}", True, (255, 255, 255)), (24, 52))

        # Score and Objective
        label = self.font.render(f"Kills: {self.player.kills}", True, (255, 255, 255))
        self.screen.blit(label, (WINDOW_W - 180, 24))
        objective = self.small_font.render("Destroy all enemies in the bunker.", True, (220, 220, 220))
        self.screen.blit(objective, (WINDOW_W // 2 - objective.get_width() // 2, 24))

        # Weapon overlay
        w = 260
        h = 180
        x = WINDOW_W - w - 40
        y = WINDOW_H - h - 25
        weapon = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(weapon, (30, 30, 30, 200), (20, 30, 180, 90))
        pygame.draw.rect(weapon, (100, 100, 100, 180), (75, 10, 80, 100))
        pygame.draw.rect(weapon, (180, 180, 180, 220), (88, 95, 56, 40))
        self.screen.blit(weapon, (x, y))

        if self.flash > 0:
            flash = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
            pygame.draw.circle(flash, (255, 220, 160, int(self.flash * 220)), (WINDOW_W // 2, WINDOW_H // 2), 220)
            self.screen.blit(flash, (0, 0))

        if self.game_over:
            overlay = pygame.Surface((WINDOW_W, WINDOW_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
            text = self.big_font.render("YOU DIED", True, (255, 80, 80))
            self.screen.blit(text, (WINDOW_W // 2 - text.get_width() // 2, WINDOW_H // 2 - 80))
            hint = self.font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
            self.screen.blit(hint, (WINDOW_W // 2 - hint.get_width() // 2, WINDOW_H // 2 + 20))

    def update(self, dt):
        if self.game_over:
            return
        self.move_player(dt)
        self.update_enemies(dt)
        self.player.fire_cooldown -= dt
        if self.flash > 0:
            self.flash -= dt

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]) and self.player.fire_cooldown <= 0:
            self.player.fire_cooldown = 0.18
            self.shoot()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x != WINDOW_W // 2 or mouse_y != WINDOW_H // 2:
            dx = mouse_x - WINDOW_W // 2
            self.player.angle += dx * 0.0025
            pygame.mouse.set_pos((WINDOW_W // 2, WINDOW_H // 2))

    def draw_minimap(self):
        map_w = len(MAP[0])
        map_h = len(MAP)
        cell = 12
        minimap_x = 24
        minimap_y = WINDOW_H - (map_h * cell) - 24
        for row_idx, row in enumerate(MAP):
            for col_idx, tile in enumerate(row):
                color = (30, 30, 30) if tile == "1" else (80, 80, 80)
                pygame.draw.rect(self.screen, color, (minimap_x + col_idx * cell, minimap_y + row_idx * cell, cell - 1, cell - 1))
        pygame.draw.circle(self.screen, (255, 255, 255), (int(minimap_x + self.player.x * cell), int(minimap_y + self.player.y * cell)), 4)
        for enemy in self.enemies:
            if enemy.alive:
                pygame.draw.circle(self.screen, (255, 80, 80), (int(minimap_x + enemy.x * cell), int(minimap_y + enemy.y * cell)), 3)

    def render(self):
        self.draw_scene()
        self.draw_enemies()
        self.draw_minimap()
        self.draw_hud()
        pygame.display.flip()

    def loop(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r and self.game_over:
                        self.__init__()
            self.update(dt)
            self.render()
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.loop()


if __name__ == "__main__":
    main()
