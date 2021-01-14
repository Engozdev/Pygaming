import pygame
import sys
import os
import random

FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        pass
        # image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/map/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, f=False):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        if f:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x - 1, tile_height * pos_y - 61)
        else:
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.frames = [pygame.transform.scale(load_image('hero_1.png'), (48, 100)),
                       pygame.transform.scale(load_image('hero_2.png'), (48, 100)),
                       pygame.transform.scale(load_image('hero_3.png'), (48, 100)),
                       pygame.transform.scale(load_image('hero_2.png'), (48, 100))]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 1, tile_height * pos_y - 50)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = pos_x, pos_y = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 1, tile_height * pos_y - 50)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def show_task(ques_num):
    image_path = lvl[seed[tek]][0][ques_num]
    question = lvl[seed[tek]][1][ques_num]
    correct_answer = lvl[seed[tek]][2][ques_num].lower()

    fon = pygame.transform.scale(load_image('Terminal.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.SysFont('Arial', 30)
    question = '>' + question
    quest = font.render(question, False, (255, 255, 255))
    screen.blit(quest, (300, 270))
    hint = font.render('>Ваш ответ', False, (255, 255, 255))
    screen.blit(hint, (300, 550))

    all_sprites = pygame.sprite.Group()
    task = pygame.sprite.Sprite()
    task.image = load_image(image_path)
    task.rect = 900, 200
    all_sprites.add(task)
    alphabet = {113: 'й', 119: 'ц', 101: 'у', 114: 'к', 116: 'е', 121: 'н', 117: 'г', 105: 'ш', 111: 'щ', 112: 'з',
                1093: 'х', 1098: 'ъ', 97: 'ф', 115: 'ы', 100: 'в', 102: 'а', 103: 'п', 104: 'р', 106: 'о', 107: 'л',
                108: 'д', 1078: 'ж', 1101: 'э', 122: 'я', 120: 'ч', 99: 'с', 118: 'м', 98: 'и', 110: 'т', 109: 'ь',
                1073: 'б', 1102: 'ю', 1105: 'ё', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7',
                56: '8', 57: '9', 48: '0', 45: '-', 46: ',', 32: ' '}
    ans = '>'
    corr_flag = ''
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == 13:
                    ans_copy = ans
                    ans = '>'
                    screen.blit(fon, (0, 0))
                    all_sprites.draw(screen)
                    if ans_copy[1:] == correct_answer:
                        pygame.draw.circle(screen, pygame.Color('green'), (1000, 700), 100)
                        lvl[seed[tek]][3][ques_num] = True
                        corr_flag = True
                    else:
                        corr_flag = False
                        pygame.draw.circle(screen, pygame.Color('red'), (1000, 700), 100)
                    screen.blit(quest, (300, 270))
                    screen.blit(hint, (300, 550))
                    ans_copy = ''
                elif event.key == 8:
                    ans = ans[:-1]
                    if '>' not in ans:
                        ans = '>' + ans
                    screen.blit(fon, (0, 0))
                    all_sprites.draw(screen)
                    if isinstance(corr_flag, bool):
                        if corr_flag:
                            pygame.draw.circle(screen, pygame.Color('green'), (1000, 700), 100)
                        else:
                            pygame.draw.circle(screen, pygame.Color('red'), (1000, 700), 100)
                    screen.blit(quest, (300, 270))
                    screen.blit(hint, (300, 550))
                elif event.key == 27:
                    return
                else:
                    try:
                        ans += alphabet[event.key]
                    except Exception:
                        pass
            all_sprites.draw(screen)
            display_ans = font.render(ans, False, (255, 255, 255))
            screen.blit(display_ans, (300, 610))
            pygame.display.flip()
            pygame.display.flip()
            clock.tick(FPS)


def generate_level(level, f=0):
    global sprite_group
    new_player, x, y = None, None, None
    hx, hy = 0, 0
    hx1, hy1, hx2, hy2 = 0, 0, 0, 0
    sprite_group = pygame.sprite.Group()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                hx, hy = x, y
            elif level[y][x] == 'V':
                hx2, hy2 = x, y
            elif level[y][x] == 'X':
                hx1, hy1 = x, y
            elif level[y][x] == 'B':
                Tile('0-0', x, y)
            elif level[y][x] == '1' or level[y][x] == '2':
                Tile('dor', x, y)
            elif level[y][x] == 'D':
                s, k = 0, 0
                for i in lvl[seed[tek]][3]:
                    k += 1
                    if i:
                        s += 1
                st = str(k) + '-' + str(s)
                Tile(st, x, y)
            elif level[y][x] == '?' or level[y][x] == 'f':
                Tile('kvest', x, y, f=True)
    if f == 1:
        return hx1, hy1, x, y
    elif f == 2:
        return hx2, hy2, x, y
    return hx, hy, x, y


def new_lvl(nam):
    global tek, level_map, max_x, max_y, seed, hero, fon
    f = 0
    if nam == '1':
        tek -= 1
        f = 1
    elif nam == '2':
        s, k = 0, 0
        for i in lvl[seed[tek]][3]:
            k += 1
            if i:
                s += 1
        if s == k:
            tek += 1
            f = 2
    if f:
        name = 'map_' + seed[tek] + '.txt'
        level_map = load_level(name)
        name = 'map/' + seed[tek] + '_fon.jpg'
        fon = load_image(name)
        hx, hy, max_x, max_y = generate_level(level_map, f=f)
        hero.move(hx, hy)


def move(heros, movement=None):
    global running
    x, y = heros.pos
    new_x, new_y = x, y
    if movement == 'left':
        if x > 0 and level_map[y][x - 1] != '#':
            new_x, new_y = (x - 1, y)
        elif x > 0 and y - 1 >= 0 and level_map[y - 1][x - 1] != '#':
            new_x, new_y = (x - 1, y - 1)
    elif movement == 'right':
        if x < max_x and level_map[y][x + 1] != '#':
            new_x, new_y = (x + 1, y)
        elif x < max_x and y - 1 >= 0 and level_map[y - 1][x + 1] != '#':
            new_x, new_y = (x + 1, y - 1)
    elif movement == None:
        if y < max_y - 1 and level_map[y + 1][x] != '#':
            new_x, new_y = (x, y + 1)
    nam = level_map[new_y][new_x]
    if nam == '1' or nam == 'B':
        new_lvl('1')
    elif nam == '2' or nam == 'D':
        new_lvl('2')
    elif nam == 'R':
        running = False
    else:
        heros.move(new_x, new_y)


def check_position(hero):
    x, y = hero.pos
    f = False
    if level_map[y][x] == '?':
        ques_num = lvl[seed[tek]][4][(y, x)]
        f = True
    elif x >= 1 and level_map[y][x - 1] == '?':
        ques_num = lvl[seed[tek]][4][(y, x - 1)]
        f = True
    elif x <= max_x and level_map[y][x + 1] == '?':
        ques_num = lvl[seed[tek]][4][(y, x + 1)]
        f = True
    if f:
        show_task(ques_num)
        generate_level(level_map)

def start_screen():
    fon = load_image('start_screen_1.jpg')
    k = 1
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if k < 3:
                    k += 1
                    name = 'start_screen_' + str(k) + '.jpg'
                    fon = load_image(name)
                    screen.blit(fon, (0, 0))
                else:
                    return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    tile_images = {
        'dor': pygame.transform.scale(load_image('box_n.png'), (50, 50)),
        '0-0': pygame.transform.scale(load_image('box_v.png'), (50, 50)),
        '1-0': load_image('box_1_0.png'),
        '1-1': load_image('box_1_1.png'),
        '2-0': load_image('box_2_0.png'),
        '2-1': load_image('box_2_1.png'),
        '2-2': load_image('box_2_2.png'),
        '3-0': load_image('box_3_0.png'),
        '3-1': load_image('box_3_1.png'),
        '3-2': load_image('box_3_2.png'),
        '3-3': load_image('box_3_3.png'),
        'kvest': pygame.transform.scale(load_image('kvest.png'), (52, 111)),
        'wall': pygame.transform.scale(load_image('kodred.png'), (50, 50))
    }
    tile_width = tile_height = 50
    pygame.init()
    pygame.display.set_caption('Subvectio certamine')
    size = width, height = 1500, 1000
    FPS = 50

    lvl = {
        '0': [['puzzle/lol.jpg', 'puzzle/twitter.png'], ['Как называется этот бренд?'] * 2, ['Яндекс Еда', 'Твиттер'], [False] * 2, {(13, 0): 0, (6, 27): 1}],
        '1': [['puzzle/Big_Tasty.jpg', 'puzzle/cheezburger.jpg'], ['Какое блюдо изображено на картинке?'] * 2,
              ['Биг Тести', 'чизбургер'], [False] * 2, {(15, 14): 0, (13, 23): 1}],
        '2': [['puzzle/vopper_barbeku.png', 'puzzle/king.png'], ['Какое блюдо изображено на картинке?'] * 2,
              ['Воппер барбекю', 'чикин кинг'], [False] * 2, {(9, 8): 0, (9, 26): 1}],
        '3': [['puzzle/twister.png', 'puzzle/shaurma.jpg', 'puzzle/pepperoni.png'],
              ['Какое блюдо изображено на картинке?'] * 3, ['твистер', 'шаурма', 'пепперони'],
              [False] * 3, {(10, 17): 0, (13, 11): 1, (15, 7): 2}],
        '4': [['puzzle/Pepsi.png', 'puzzle/Happy_Meal.png'],
              ['Как называется этот бренд?',
               'Какое блюдо изображено на картинке?'], ['пепси', 'Хеппи мил'],
              [False] * 2, {(3, 12): 0, (9, 12): 1}],
        '5': [['puzzle/DeliveryClub.png'], ['Кто/что это?'], ['КОНКУРЕНТЫ'], [False], {(17, 18): 0}],
        'k': [[], [], [False] * 0, {}]
    }

    screen = pygame.display.set_mode(size)
    running = True
    seed = ['1', '2', '3', '4', '5']
    random.shuffle(seed)
    seed = ['0'] + seed + ['k']
    clock = pygame.time.Clock()
    level_map = load_level('map_0.txt')
    tek = 0
    hx, hy, max_x, max_y = generate_level(level_map)
    hero = Player(hx, hy)
    ticks, speed = 0, 25
    fon = load_image('map/0_fon.jpg')
    ter = True
    # fon = pygame.transform.scale(load_image('fon3.jpg'), (width, height))
    start_screen()
    while running:
        keys = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                check_position(hero)
        # screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        if ticks == speed:
            hero.update()
            ticks = 0
        if ticks % 6 == 0:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move(hero, 'left')
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move(hero, 'right')
        if ticks % 3 == 0 and ter:
            move(hero)
        ticks += 1
        all_sprites.draw(screen)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
