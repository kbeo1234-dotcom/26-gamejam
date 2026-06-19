import pygame
import pymunk
import random
from ObstacleWall import *
from Ball import *
from Peg import *

WIDTH, HEIGHT = 600, 800
FPS = 60
GRAVITY = (0, 900)

MONEY = 5
BALLCOUNT = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("pachinko")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)


def start():
    screen.fill((20, 20, 40))

    title = font.render("PACHINKO GAME", True, (255, 215, 0))
    screen.blit(title, (WIDTH / 2 - title.get_width() / 2, HEIGHT / 2 - 150))

    guide_lines = [
        "GAME GUIDE",
        "Press the SPACE bar to shoot the balls.",
        "The game ends when you run out of money.",
        "May luck be on your side!"
    ]

    start_y = HEIGHT / 2 - 50
    line_spacing = 40

    for i, line in enumerate(guide_lines):
        color = (255, 100, 100) if i == 0 else (200, 200, 200)
        text_surface = font.render(line, True, color)
        text_x = WIDTH / 2 - text_surface.get_width() / 2
        text_y = start_y + (i * line_spacing)
        screen.blit(text_surface, (text_x, text_y))

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
def main():
    global MONEY

    space = pymunk.Space()
    space.gravity = GRAVITY
    score_board = [5, -25, 50, -25, 5]
    basket_ratios = [3, 3, 1, 3, 3]

    pegs = []
    for row in range(5, 16):
        for col in range(row):
            x = WIDTH // 2 + (col - row / 2) * 40 + 20
            y = row * 45 + 50

    for row in range(5, 16):
        for col in range(row):
            x = WIDTH // 2 + (col - row / 2) * 40 + 20
            y = row * 45 + 50
            pegs.append(Peg(space, x, y))

    walls = []

    total_ratio = sum(basket_ratios)
    unit_width = WIDTH / total_ratio

    wall_boundaries = []
    current_x = 0

    for i in range(len(basket_ratios) - 1):
        current_x += basket_ratios[i] * unit_width
        wall_boundaries.append(current_x)

        wall_y = HEIGHT - 60
        wall_w = 10
        wall_h = 120
        walls.append(ObstacleWall(space, current_x, wall_y, wall_w, wall_h))

    wall_boundaries.append(WIDTH)
    balls = []
    current_money = MONEY

    last_spawn_time = 0
    spawn_delay = 100

    earn_btn_rect = pygame.Rect(400, 15, 180, 40)
    earn_btn_text = font.render("Go Earn Money", True, (255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if earn_btn_rect.collidepoint(event.pos):
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()

            if current_time - last_spawn_time > spawn_delay and current_money > 0:
                current_money -= 1
                start_x = WIDTH // 2 + random.randint(-20, 20)
                balls.append(Ball(space, start_x, 30))

                last_spawn_time = current_time

        space.step(1 / FPS)
        screen.fill((20, 20, 40))

        for peg in pegs:
            peg.draw(screen)

        for wall in walls:
            wall.draw(screen)

        for ball in balls[:]:
            ball.draw(screen)

            if ball.body.position.y > HEIGHT - 20:
                ball_x = ball.body.position.x
                basket_index = 0

                for boundary in wall_boundaries:
                    if ball_x < boundary:
                        break
                    basket_index += 1

                if basket_index >= len(score_board):
                    basket_index = len(score_board) - 1

                if current_money < 0:
                    current_money = 0
                    running = False
                else:
                    current_money += score_board[basket_index]

                space.remove(ball.body, ball.shape)
                balls.remove(ball)
        money_text = font.render(f"MONEY: {current_money}", True, (255, 255, 255))
        screen.blit(money_text, (20, 20))

        mouse_pos = pygame.mouse.get_pos()
        earn_btn_color = (0, 150, 0) if earn_btn_rect.collidepoint(mouse_pos) else (0, 200, 0)
        pygame.draw.rect(screen, earn_btn_color, earn_btn_rect)
        screen.blit(earn_btn_text, earn_btn_text.get_rect(center=earn_btn_rect.center))

        pygame.display.flip()
        clock.tick(FPS)
        MONEY = current_money
def end():
    global MONEY
    current_money = MONEY

    button_rect = pygame.Rect(200, 150, 200, 80)
    button_text = font.render("Working!", True, (255, 255, 255))

    button_rect_2 = pygame.Rect(200, 280, 200, 80)
    button_text_2 = font.render("ReStart!", True, (255, 255, 255))

    button_rect_3 = pygame.Rect(200, 410, 200, 80)
    button_text_3 = font.render("Exit", True, (255, 255, 255))

    running = True
    play_again = False

    while running:
        screen.fill((20, 20, 40))

        # 💡 [수정됨] 마우스 위치 확인 및 색상 결정은 이벤트 루프 밖에서 매 프레임 실행합니다.
        mouse_pos = pygame.mouse.get_pos()

        color_1 = (0, 100, 200) if button_rect.collidepoint(mouse_pos) else (0, 255, 255)
        color_2 = (200, 50, 50) if button_rect_2.collidepoint(mouse_pos) else (255, 100, 100)
        color_3 = (100, 100, 100) if button_rect_3.collidepoint(mouse_pos) else (150, 150, 150)

        # 단발성 이벤트(클릭, 종료)만 for문 안에서 처리합니다.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                play_again = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    current_money += 1

                if button_rect_2.collidepoint(event.pos):
                    running = False
                    play_again = True

                if button_rect_3.collidepoint(event.pos):
                    running = False
                    play_again = False

        # 그리기 파트
        pygame.draw.rect(screen, color_1, button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        pygame.draw.rect(screen, color_2, button_rect_2)
        screen.blit(button_text_2, button_text_2.get_rect(center=button_rect_2.center))

        pygame.draw.rect(screen, color_3, button_rect_3)
        screen.blit(button_text_3, button_text_3.get_rect(center=button_rect_3.center))

        money_text = font.render(f"MONEY: {current_money}", True, (255, 255, 255))
        screen.blit(money_text, (20, 20))

        pygame.display.flip()

    MONEY = current_money
    return play_again
if __name__ == "__main__":
    start()

    while True:
        main()
        if not end():
            break
    pygame.quit()