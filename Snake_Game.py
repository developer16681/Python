"""
Snake Game - built with Pygame
Controls: Arrow keys to move, ESC to quit, R to restart after game over
"""

import pygame
import random
import sys

# --- Config ---
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 5 
""" 
Change this value to adjust the speed of the snake in the game.
 Higher values make the snake move faster,
 while lower values make it move slower.
 """

# Colors
BLACK = (20, 20, 20)
GREEN = (50, 200, 80)
DARK_GREEN = (30, 150, 60)
RED = (220, 60, 60)
WHITE = (240, 240, 240)
GRAY = (60, 60, 60)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def move(self):
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    def set_direction(self, new_dir):
        # Prevent reversing directly into itself
        dx, dy = self.direction
        ndx, ndy = new_dir
        if (dx, dy) == (-ndx, -ndy):
            return
        self.direction = new_dir

    def check_self_collision(self):
        return self.head() in self.body[1:]

    def check_wall_collision(self):
        x, y = self.head()
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos

    def respawn(self, snake_body):
        self.position = self.random_position(snake_body)

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)


def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_text_center(surface, text, font, color, y_offset=0):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(rendered, rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont("arial", 36, bold=True)
    font_small = pygame.font.SysFont("arial", 22)

    def reset_game():
        snake = Snake()
        food = Food(snake.body)
        return snake, food, 0, False  # snake, food, score, game_over

    snake, food, score, game_over = reset_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    snake.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.set_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.set_direction(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    snake, food, score, game_over = reset_game()

        if not game_over:
            snake.move()

            if snake.check_wall_collision() or snake.check_self_collision():
                game_over = True

            if snake.head() == food.position:
                snake.grow(1)
                score += 1
                food.respawn(snake.body)

        # --- Draw ---
        screen.fill(BLACK)
        draw_grid(screen)
        food.draw(screen)
        snake.draw(screen)

        score_surf = font_small.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        if game_over:
            draw_text_center(screen, "GAME OVER", font_big, WHITE, y_offset=-20)
            draw_text_center(screen, "Press R to restart or ESC to quit", font_small, WHITE, y_offset=20)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()