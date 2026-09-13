"""
Snake Game
----------
A classic Snake game built with Python and Pygame.

Controls:
    Arrow Keys / WASD - Move the snake
    P                 - Pause / Resume
    R                 - Restart after Game Over
    Q / ESC           - Quit

Run:
    python snake_game.py
"""

import pygame
import random
import sys

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS_START = 8          # starting speed
FPS_MAX = 20            # top speed
SPEEDUP_EVERY = 5        # increase speed every N food eaten

# Colors (R, G, B)
COLOR_BG = (18, 18, 18)
COLOR_GRID = (28, 28, 28)
COLOR_SNAKE_HEAD = (76, 175, 80)
COLOR_SNAKE_BODY = (56, 142, 60)
COLOR_FOOD = (229, 57, 53)
COLOR_TEXT = (240, 240, 240)
COLOR_SHADOW = (0, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        cx, cy = GRID_WIDTH // 2, GRID_HEIGHT // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow_pending = 0

    def set_direction(self, new_dir):
        # Prevent the snake from reversing directly into itself
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_direction = new_dir

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, amount=1):
        self.grow_pending += amount

    @property
    def head(self):
        return self.body[0]

    def collides_with_self(self):
        return self.head in self.body[1:]

    def collides_with_wall(self):
        x, y = self.head
        return x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT


class Food:
    def __init__(self, snake_body):
        self.position = (0, 0)
        self.respawn(snake_body)

    def respawn(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                self.position = pos
                return


def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, COLOR_GRID, (0, y), (SCREEN_WIDTH, y))


def draw_cell(surface, pos, color, inset=1):
    x, y = pos
    rect = pygame.Rect(
        x * CELL_SIZE + inset,
        y * CELL_SIZE + inset,
        CELL_SIZE - inset * 2,
        CELL_SIZE - inset * 2,
    )
    pygame.draw.rect(surface, color, rect, border_radius=4)


def draw_text_centered(surface, text, font, color, y, shadow=True):
    if shadow:
        shadow_surf = font.render(text, True, COLOR_SHADOW)
        shadow_rect = shadow_surf.get_rect(center=(SCREEN_WIDTH // 2 + 2, y + 2))
        surface.blit(shadow_surf, shadow_rect)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y))
    surface.blit(text_surf, text_rect)


def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("arial", 42, bold=True)
    font_med = pygame.font.SysFont("arial", 24, bold=True)
    font_small = pygame.font.SysFont("arial", 18)

    snake = Snake()
    food = Food(snake.body)

    score = 0
    high_score = 0
    speed = FPS_START
    paused = False
    game_over = False

    key_to_dir = {
        pygame.K_UP: UP, pygame.K_w: UP,
        pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
        pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
        pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    }

    while True:
        # --- Event handling -------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

                if event.key in key_to_dir and not game_over:
                    snake.set_direction(key_to_dir[event.key])

                if event.key == pygame.K_p and not game_over:
                    paused = not paused

                if event.key == pygame.K_r and game_over:
                    snake.reset()
                    food.respawn(snake.body)
                    score = 0
                    speed = FPS_START
                    game_over = False
                    paused = False

        # --- Update -----------------------------------------------------------
        if not paused and not game_over:
            snake.move()

            if snake.collides_with_wall() or snake.collides_with_self():
                game_over = True
                high_score = max(high_score, score)

            elif snake.head == food.position:
                snake.grow()
                food.respawn(snake.body)
                score += 1
                if score % SPEEDUP_EVERY == 0:
                    speed = min(FPS_MAX, speed + 1)

        # --- Draw ---------------------------------------------------------
        screen.fill(COLOR_BG)
        draw_grid(screen)

        draw_cell(screen, food.position, COLOR_FOOD)

        for i, segment in enumerate(snake.body):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            draw_cell(screen, segment, color)

        score_surf = font_small.render(f"Score: {score}   High Score: {high_score}", True, COLOR_TEXT)
        screen.blit(score_surf, (8, 6))

        if paused and not game_over:
            draw_text_centered(screen, "PAUSED", font_big, COLOR_TEXT, SCREEN_HEIGHT // 2)
            draw_text_centered(screen, "Press P to resume", font_small, COLOR_TEXT, SCREEN_HEIGHT // 2 + 40)

        if game_over:
            draw_text_centered(screen, "GAME OVER", font_big, COLOR_FOOD, SCREEN_HEIGHT // 2 - 20)
            draw_text_centered(screen, f"Score: {score}", font_med, COLOR_TEXT, SCREEN_HEIGHT // 2 + 25)
            draw_text_centered(screen, "Press R to restart or Q to quit", font_small, COLOR_TEXT, SCREEN_HEIGHT // 2 + 55)

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
