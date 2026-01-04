import pygame
import random
import sys

pygame.init()

# ================== 基本設定 ==================
WIDTH, HEIGHT = 640, 480
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 24)
BIG_FONT = pygame.font.SysFont("arial", 40)

# 顏色
BG = (30, 30, 40)
GREEN = (80, 200, 120)
DARK_GREEN = (60, 160, 100)
RED = (220, 60, 60)
YELLOW = (240, 200, 60)
BLUE = (80, 150, 220)
GRAY = (120, 120, 120)
WHITE = (240, 240, 240)

# ================== UI 按鈕 ==================
class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse) else DARK_GREEN
        shadow = self.rect.move(4, 4)
        pygame.draw.rect(screen, (20,20,20), shadow, border_radius=10)
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        txt = FONT.render(self.text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

# ================== 愛心 ==================
def draw_heart(x, y, size=8):
    pygame.draw.circle(screen, RED, (x, y), size)
    pygame.draw.circle(screen, RED, (x + size*2, y), size)
    pygame.draw.polygon(screen, RED, [
        (x - size, y),
        (x + size*3, y),
        (x + size, y + size*3)
    ])

# ================== 遊戲物件 ==================
def random_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

def draw_snake(snake):
    for i, (x, y) in enumerate(snake):
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(screen, GREEN, rect, border_radius=6)
        if i == 0:
            pygame.draw.circle(screen, (0,0,0), (x+6, y+6), 3)
            pygame.draw.circle(screen, (0,0,0), (x+CELL-6, y+6), 3)

def draw_fruit(f):
    pygame.draw.circle(
        screen, f["color"],
        (f["pos"][0] + CELL//2, f["pos"][1] + CELL//2),
        CELL//2 - 2
    )

# ================== 主選單 ==================
def menu():
    buttons = [
        Button((220, 200, 200, 50), "Easy"),
        Button((220, 260, 200, 50), "Normal"),
        Button((220, 320, 200, 50), "Hard")
    ]

    while True:
        screen.fill(BG)
        title = BIG_FONT.render("Snake Game", True, WHITE)
        screen.blit(title, title.get_rect(center=(WIDTH//2, 120)))

        for b in buttons:
            b.draw()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if buttons[0].clicked(event):
                return "easy"
            if buttons[1].clicked(event):
                return "normal"
            if buttons[2].clicked(event):
                return "hard"

# ================== 主遊戲 ==================
def game(difficulty):
    snake = [(100,100), (80,100), (60,100)]
    direction = (0,0)
    started = False
    lives = 3
    score = 0

    fruits = []
    for _ in range(3):
        fruits.append({
            "pos": random_pos(),
            "color": random.choice([RED, YELLOW, BLUE]),
            "score": random.choice([1, 2, 3])
        })

    obstacles = []
    movers = []

    if difficulty == "normal":
        obstacles = [random_pos() for _ in range(5)]
    if difficulty == "hard":
        obstacles = [random_pos() for _ in range(7)]
        movers = [{"pos": random_pos(), "dir": random.choice([(20,0),(-20,0),(0,20),(0,-20)])}]

    speed = {"easy": 7, "normal": 9, "hard": 11}[difficulty]

    while True:
        clock.tick(speed)
        screen.fill(BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                started = True
                if event.key == pygame.K_UP:
                    direction = (0, -CELL)
                elif event.key == pygame.K_DOWN:
                    direction = (0, CELL)
                elif event.key == pygame.K_LEFT:
                    direction = (-CELL, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (CELL, 0)

        if started:
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            snake.insert(0, head)

            if head in [f["pos"] for f in fruits]:
                for f in fruits:
                    if f["pos"] == head:
                        score += f["score"]
                        fruits.remove(f)
                        fruits.append({
                            "pos": random_pos(),
                            "color": random.choice([RED, YELLOW, BLUE]),
                            "score": random.choice([1, 2, 3])
                        })
                        break
            else:
                snake.pop()

            if (
                head[0] < 0 or head[0] >= WIDTH or
                head[1] < 0 or head[1] >= HEIGHT or
                head in snake[1:] or
                head in obstacles
            ):
                lives -= 1
                snake = [(100,100), (80,100), (60,100)]
                direction = (0,0)
                started = False

        # 移動障礙（困難）
        for m in movers:
            m["pos"] = (m["pos"][0] + m["dir"][0], m["pos"][1] + m["dir"][1])
            if m["pos"][0] < 0 or m["pos"][0] >= WIDTH:
                m["dir"] = (-m["dir"][0], m["dir"][1])
            if m["pos"][1] < 0 or m["pos"][1] >= HEIGHT:
                m["dir"] = (m["dir"][0], -m["dir"][1])
            if snake[0] == m["pos"]:
                lives -= 1

        # 畫東西
        for f in fruits:
            draw_fruit(f)

        for o in obstacles:
            pygame.draw.rect(screen, GRAY, (*o, CELL, CELL), border_radius=5)

        for m in movers:
            pygame.draw.rect(screen, GRAY, (*m["pos"], CELL, CELL), border_radius=5)

        draw_snake(snake)

        for i in range(lives):
            draw_heart(20 + i*30, 20)

        score_txt = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(score_txt, (WIDTH-140, 15))

        if lives <= 0:
            return

        pygame.display.update()

# ================== 主流程 ==================
while True:
    diff = menu()
    game(diff)
