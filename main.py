import pygame
import sys
import os
import pyautogui as pg
from task import MyWidget
from PyQt5.QtWidgets import QApplication

def print_result(text, x, y):
    font = pygame.font.Font(None, 50)
    text = font.render(text, True, (100, 255, 100))
    screen.blit(text, (x, y))


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)




def check_position(hero):
    x, y = hero.pos
    positions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    for i, j in positions:
        if level_map[y + i][x + j] == '?':
            ques_num = coordinate[(y + i, x + j)]
            bool_answers[ques_num] = True
            app = QApplication(sys.argv)
            ex = MyWidget(pictures[ques_num], answers[ques_num])
            ex.show()
            app.exec()
        if level_map[y + i][x + j] == '$':
            password = pg.prompt(text=f'Введите первые буквы ответов на загадки ({len(pictures)})', title='exam')
            if password is not None:
                if set(password.lower()) == answer_letters:
                    pg.alert(text='Congratulations, you have successfully passed this level !!!', button='OK')
                else:
                    pg.alert(text='You lose! Think about', button='OK')


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'door': load_image('new_door.jpg'),
    'task': load_image('task_wall.jpg')
}
player_image = load_image('main_hero.jpg')

tile_width = tile_height = 50
pygame.init()
size = WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hero moving')
FPS = 50
clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
hero_group = pygame.sprite.Group()
# start_screen()
level_map = load_level('map.txt')
pictures = ['data/nepal.png', 'data/spain.jpg']
answers = ['Непал', 'Испания']
bool_answers = [False] * len(answers)
user_answers = list()
answer_letters = {'н', 'и'}
coordinate = {(6, 15): 0, (9, 15): 1}
running = True
player, max_x, max_y = generate_level(load_level('map.txt'))
task_flag = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            task_flag = True
            if event.key == pygame.K_UP:
                move(player, 'up')
            elif event.key == pygame.K_DOWN:
                move(player, 'down')
            elif event.key == pygame.K_LEFT:
                move(player, 'left')
            elif event.key == pygame.K_RIGHT:
                move(player, 'right')
            elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_LCTRL:
                for i in range(len(bool_answers)):
                    if bool_answers[i] and answers[i] not in user_answers:
                        user_answers.append(answers[i])
    screen.fill((0, 0, 0))
    sprite_group.draw(screen)
    hero_group.draw(screen)
    x_coord, y_coord = 900, 100
    for a in user_answers:
        print_result(a, x_coord, y_coord)
        y_coord += 100
    pygame.display.flip()
    if task_flag:
        check_position(player)
        task_flag = False
    clock.tick(FPS)
pygame.quit()
