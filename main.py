import pygame
from copy import deepcopy
from random import choice, randint

WIDHT, HEGDTH = 10, 20
TILE = 45
GAME_RES = WIDHT * TILE, HEGDTH * TILE
size = 750, 940
FPS = 60

pygame.init()
screen = pygame.display.set_mode(size)
game_sceen = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

pole = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDHT) for y in range(HEGDTH)]

figures_pos = [[(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + WIDHT // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
rect_figure = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(WIDHT)] for j in range(HEGDTH)]

anim, an_speed, anim_block = 0, 60, 2000

back, game_bg = pygame.image.load('img/bg.jpg').convert(), pygame.image.load('img/bg2.jpg').convert()

main_font = pygame.font.Font('font/Montserrat.ttf', 65)
font = pygame.font.Font('font/Montserrat.ttf', 45)

text_1 = main_font.render('TETRIS', True, pygame.Color('#f2f020'))
tex_2 = font.render('score:', True, pygame.Color('green'))
title_record = font.render('record:', True, pygame.Color('purple'))


def get_color():
    return (randint(30, 255), randint(30, 255), randint(30, 255))


fig_now, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


def check_borders():
    if fig_now[i].x < 0 or fig_now[i].x > WIDHT - 1:
        return False
    elif fig_now[i].y > HEGDTH - 1 or field[fig_now[i].y][fig_now[i].x]:
        return False
    return True


while True:
    record = get_record()
    move_x, rotate = 0, False
    screen.blit(back, (0, 0))
    screen.blit(game_sceen, (20, 20))
    game_sceen.blit(game_bg, (0, 0))
    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_x = -1
            elif event.key == pygame.K_RIGHT:
                move_x = 1
            elif event.key == pygame.K_DOWN:
                anim_block = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # move x
    figure_old = deepcopy(fig_now)
    for i in range(4):
        fig_now[i].x += move_x
        if not check_borders():
            fig_now = deepcopy(figure_old)
            break
    # move y
    anim += an_speed
    if anim > anim_block:
        anim = 0
        figure_old = deepcopy(fig_now)
        for i in range(4):
            fig_now[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                fig_now, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_block = 2000
                break
    # Поворот фигуры
    center = fig_now[0]
    figure_old = deepcopy(fig_now)
    if rotate:
        for i in range(4):
            x = fig_now[i].y - center.y
            y = fig_now[i].x - center.x
            fig_now[i].x = center.x - x
            fig_now[i].y = center.y + y
            if not check_borders():
                fig_now = deepcopy(figure_old)
                break
    # проверка линии
    line, lines = HEGDTH - 1, 0
    for row in range(HEGDTH - 1, -1, -1):
        count = 0
        for i in range(WIDHT):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < WIDHT:
            line -= 1
        else:
            an_speed += 3
            lines += 1
    # обновление счета
    score += scores[lines]
    # отрисовка поля
    for i_rect in pole:
        pygame.draw.rect(game_sceen, (200, 200, 200), i_rect, 1)
    # отрисовка фигуры
    for i in range(4):
        x = fig_now[i].x * TILE
        y = fig_now[i].y * TILE
        rect_figure.x = int(x)
        rect_figure.y = int(y)
        pygame.draw.rect(game_sceen, color, rect_figure)

    for y, raw in enumerate(field):
        for x, color_1 in enumerate(raw):
            if color_1:
                rect_figure.x = x * TILE
                rect_figure.y = y * TILE
                pygame.draw.rect(game_sceen, color_1, rect_figure)
    # отрисовка следующей фигуры
    for i in range(4):
        rect_figure.x = next_figure[i].x * TILE + 380
        rect_figure.y = next_figure[i].y * TILE + 185
        pygame.draw.rect(screen, next_color, rect_figure)
    # отрисовка текста
    screen.blit(text_1, (490, 10))
    screen.blit(tex_2, (535, 780))
    screen.blit(font.render(str(score), True, pygame.Color('#ffffff')), (550, 840))
    screen.blit(title_record, (525, 650))
    screen.blit(font.render(record, True, pygame.Color('gold')), (550, 710))
    # проигрыш
    for i in range(WIDHT):
        if field[0][i]:
            set_record(record, score)
            field = [[0 for _ in range(WIDHT)] for i in range(HEGDTH)]
            anim, an_speed, anim_block = 0, 60, 2000
            score = 0
            for rer in pole:
                color_rect = pygame.Color(get_color())
                pygame.draw.rect(game_sceen, color_rect, rer)
                screen.blit(game_sceen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
