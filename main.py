import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("NeonCatch")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 255, 128)
RED = (255, 60, 60)
BLACK = (0, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 100)
menu_font = pygame.font.Font(None, 50)

# Clock
clock = pygame.time.Clock()

# Game variables
catcher_width = 100
catcher_height = 20
catcher_y_offset = 50  # distance from bottom
catcher_speed = 8
score = 0
lives = 3

# Falling object setup
fall_speed = 5
spawn_timer = 0
spawn_delay = 30
objects = []  # list of (rect, color, type)

# Catcher
catcher_rect = pygame.Rect(
    WIDTH // 2 - catcher_width // 2,
    HEIGHT - catcher_height - catcher_y_offset,
    catcher_width,
    catcher_height
)

def spawn_object():
    x = random.randint(0, WIDTH - 20)
    color_type = random.choice(["blue", "red"])
    color = BLUE if color_type == "blue" else RED
    rect = pygame.Rect(x, -20, 20, 20)
    objects.append((rect, color, color_type))

def reset_game():
    global score, lives, objects
    score = 0
    lives = 3
    objects.clear()

def draw_text_center(text, font, color, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text_center("NEONCATCH", title_font, BLUE, HEIGHT // 3)
        draw_text_center("1. Start Game", menu_font, WHITE, HEIGHT // 2)
        draw_text_center("2. Quit", menu_font, WHITE, HEIGHT // 2 + 60)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

def resize_screen(w, h):
    global WIDTH, HEIGHT, screen, catcher_rect
    WIDTH, HEIGHT = w, h
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    catcher_rect.y = HEIGHT - catcher_height - catcher_y_offset

def game_loop():
    global score, lives, spawn_timer, catcher_rect

    reset_game()
    running = True

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)

        # Mouse control — catcher follows mouse X
        mouse_x, _ = pygame.mouse.get_pos()
        catcher_rect.x = mouse_x - catcher_width // 2
        catcher_rect.y = HEIGHT - catcher_height - catcher_y_offset

        # Bound catcher to screen
        catcher_rect.x = max(0, min(WIDTH - catcher_width, catcher_rect.x))

        # Spawn objects
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_object()
            spawn_timer = 0

        # Move objects
        for obj in list(objects):
            rect, color, obj_type = obj
            rect.y += fall_speed

            if rect.colliderect(catcher_rect):
                if obj_type == "blue":
                    score += 1
                else:
                    lives -= 1
                objects.remove(obj)

            elif rect.y > HEIGHT:
                objects.remove(obj)

        # Draw catcher
        pygame.draw.rect(screen, WHITE, catcher_rect)

        # Draw objects
        for rect, color, _ in objects:
            pygame.draw.rect(screen, color, rect)

        # Draw score & lives
        score_text = menu_font.render(f"Score: {score}", True, WHITE)
        lives_text = menu_font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))

        # Check game over
        if lives <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    game_over_screen()

def game_over_screen():
    while True:
        screen.fill(BLACK)
        draw_text_center("GAME OVER", title_font, RED, HEIGHT // 3)
        draw_text_center(f"Final Score: {score}", menu_font, WHITE, HEIGHT // 2)
        draw_text_center("Press ENTER to return to menu", menu_font, WHITE, HEIGHT // 2 + 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                resize_screen(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

if __name__ == "__main__":
    main_menu()
