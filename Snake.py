import pygame
import random
import json
import os

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
Starting_Speed = 7
Speed = Starting_Speed

HIGH_SCORE_FILE = "high_score.json"
f = open(HIGH_SCORE_FILE, "r")
data = json.load(f)
high_score = data.get("high_score", 0)
f.close()


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slither Quest")
font = pygame.font.SysFont("Arial", 24)

snake_pos = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
snake_color = "green"


def spawn_food():
    while True:
        pos = [random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
               random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE]
        if pos not in snake_body:
            return pos

food_pos = spawn_food()
food_color = "red"

score = 0
clock = pygame.time.Clock()
running = True
game_over_flag = False

def random_color():
    colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "orange"]
    return random.choice(colors)

def show_score():
    score_text = font.render("Score: " + str(score) + "  High Score: " + str(high_score), True, "white")
    screen.blit(score_text, (10, 10))

def reset_game():
    global snake_pos, snake_body, snake_direction, change_to, snake_color
    global food_pos, score, FPS, game_over_flag

    snake_pos = [100, 50]
    snake_body = [[100, 50], [80, 50], [60, 50]]
    snake_direction = 'RIGHT'
    change_to = snake_direction
    snake_color = "green"
    food_pos = spawn_food()
    score = 0
    Speed = Starting_Speed
    game_over_flag = False

def handle_game_over():
    global high_score, game_over_flag
    if score > high_score:
        high_score = score
        with open(HIGH_SCORE_FILE, 'w') as f:
            json.dump({"high_score": high_score}, f)

    over_text = font.render("GAME OVER - Press R to Restart", True, "white")
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - over_text.get_height() // 2))
    pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over_flag:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    change_to = 'RIGHT'
            else:
                if event.key == pygame.K_r:
                    reset_game()

    if not game_over_flag:
        snake_direction = change_to

        
        if snake_direction == 'UP':
            snake_pos[1] -= CELL_SIZE
        elif snake_direction == 'DOWN':
            snake_pos[1] += CELL_SIZE
        elif snake_direction == 'LEFT':
            snake_pos[0] -= CELL_SIZE
        elif snake_direction == 'RIGHT':
            snake_pos[0] += CELL_SIZE

        snake_body.insert(0, list(snake_pos))

        if pygame.Rect(snake_pos[0], snake_pos[1], CELL_SIZE, CELL_SIZE).colliderect(pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE)):
            score += 1
            food_pos = spawn_food()
            snake_color = random_color()
            Speed += 0.5
        else:
            snake_body.pop()

       
        if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT or snake_pos in snake_body[1:]):
            game_over_flag = True

    screen.fill("black")

    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))

    show_score()

    if game_over_flag:
        handle_game_over()

    pygame.display.update()

    clock.tick(Speed)

pygame.quit()
