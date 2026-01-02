import pygame
import random
import sys

pygame.init()

# ---------- 常數 ----------
BLOCK = 20
WIDTH, HEIGHT = 600, 400

FONT = pygame.font.SysFont("consolas", 20)
BIG_FONT = pygame.font.SysFont("consolas", 36)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (50,200,50)
RED   = (220,50,50)
BLUE  = (50,150,255)
GRAY  = (150,150,150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# ---------- 工具 ----------
def random_pos():
    return (
        random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK)
    )

# ---------- 難度選單 ----------
def difficulty_menu():
    while True:
        screen.fill(BLACK)
        screen.blit(BIG_FONT.render("Choose Difficulty", True, WHITE), (130, 60))
        screen.blit(FONT.render("1 - Easy", True, WHITE), (240, 150))
        screen.blit(FONT.render("2 - Normal", True, WHITE), (240, 190))
        screen.blit(FONT.render("3 - Hard", True, WHITE), (240, 230))
        screen.blit(FONT.render("Press 1 / 2 / 3", True, GRAY), (200, 280))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "easy"
                if event.key == pygame.K_2:
                    return "normal"
                if event.key == pygame.K_3:
                    return "hard"

# ---------- 障礙物 ----------
def generate_walls(level):
    if level == "easy":
        return []
    count = {"normal": 12, "hard": 20}[level]
    return [random_pos() for _ in range(count)]

# ---------- 主遊戲 ----------
def run_game(difficulty):
    snake = [(100,100),(80,100),(60,100)]
    direction = None   # ★ 一開始不動
    score = 0
    lives = 3
    speed = 10

    walls = generate_walls(difficulty)

    foods = [
        {"pos": random_pos(), "color": RED, "score": 10},
        {"pos": random_pos(), "color": GREEN, "score": 20},
        {"pos": random_pos(), "color": BLUE, "score": 30},
    ]

    danger = {
        "pos": random_pos(),
        "dir": random.choice([(BLOCK,0),(-BLOCK,0),(0,BLOCK),(0,-BLOCK)])
    }

    while True:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction!=(0,BLOCK):
                    direction=(0,-BLOCK)
                elif event.key == pygame.K_DOWN and direction!=(0,-BLOCK):
                    direction=(0,BLOCK)
                elif event.key == pygame.K_LEFT and direction!=(BLOCK,0):
                    direction=(-BLOCK,0)
                elif event.key == pygame.K_RIGHT and direction!=(-BLOCK,0):
                    direction=(BLOCK,0)

        # ★ 還沒按方向鍵，不移動
        if direction is None:
            screen.fill(BLACK)
            for x,y in snake:
                pygame.draw.rect(screen, GREEN,(x,y,BLOCK,BLOCK))
            for food in foods:
                pygame.draw.rect(screen, food["color"],(*food["pos"],BLOCK,BLOCK))
            for wx,wy in walls:
                pygame.draw.rect(screen, GRAY,(wx,wy,BLOCK,BLOCK))

            screen.blit(FONT.render("Press arrow key to start", True, WHITE), (170, 180))
            pygame.display.update()
            continue

        hx,hy = snake[0]
        new_head = (hx+direction[0], hy+direction[1])

        if (
            new_head[0]<0 or new_head[0]>=WIDTH or
            new_head[1]<0 or new_head[1]>=HEIGHT or
            new_head in snake or
            new_head in walls
        ):
            lives -= 1
            snake = [(100,100),(80,100),(60,100)]
            direction = None
            if lives <= 0:
                return
            continue

        snake.insert(0,new_head)
        snake.pop()

        for food in foods:
            if new_head == food["pos"]:
                score += food["score"]
                snake.append(snake[-1])
                food["pos"] = random_pos()

        if difficulty == "hard":
            dx,dy = danger["dir"]
            x,y = danger["pos"]
            nx,ny = x+dx,y+dy
            if nx<0 or nx>=WIDTH or ny<0 or ny>=HEIGHT:
                danger["dir"] = random.choice([(BLOCK,0),(-BLOCK,0),(0,BLOCK),(0,-BLOCK)])
            else:
                danger["pos"] = (nx,ny)

            if new_head == danger["pos"]:
                score = max(0, score-15)

        screen.fill(BLACK)

        for x,y in snake:
            pygame.draw.rect(screen, GREEN,(x,y,BLOCK,BLOCK))

        for food in foods:
            pygame.draw.rect(screen, food["color"],(*food["pos"],BLOCK,BLOCK))

        for wx,wy in walls:
            pygame.draw.rect(screen, GRAY,(wx,wy,BLOCK,BLOCK))

        if difficulty == "hard":
            pygame.draw.rect(screen, GRAY,(*danger["pos"],BLOCK,BLOCK))

        screen.blit(FONT.render(f"Score: {score}",True,WHITE),(10,10))
        screen.blit(FONT.render(f"Lives: {lives}",True,WHITE),(10,30))
        screen.blit(FONT.render(f"Mode: {difficulty}",True,WHITE),(10,50))

        pygame.display.update()

# ---------- Game Over ----------
def game_over_screen():
    while True:
        screen.fill(BLACK)
        screen.blit(BIG_FONT.render("GAME OVER", True, RED), (170, 150))
        screen.blit(FONT.render("R - Restart", True, WHITE), (230, 210))
        screen.blit(FONT.render("Q - Quit", True, WHITE), (230, 240))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# ---------- 主流程 ----------
while True:
    mode = difficulty_menu()
    run_game(mode)
    game_over_screen()
