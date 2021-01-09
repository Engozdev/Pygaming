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
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.abs_pos = (self.rect.x, self.rect.y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = pos_x, pos_y = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def generate_level(level, f=0):
    global sprite_group
    new_player, x, y = None, None, None
    hx, hy = 0, 0
    hx1, hy1, hx2, hy2 = 0, 0, 0, 0
    sprite_group = pygame.sprite.Group()
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                hx, hy = x, y
            elif level[y][x] == 'V':
                hx2, hy2 = x, y
            elif level[y][x] == 'X':
                hx1, hy1 = x, y
            elif level[y][x] == '1' or level[y][x] == '2':
                Tile('dor', x, y)
    if f == 1:
        return hx1, hy1, x, y
    elif f == 2:
        return hx2, hy2, x, y
    return hx, hy, x, y


def new_lvl(x, y, heros):
    global tek, level_map, max_x, max_y, seed
    nam = level_map[y][x]
    if nam == '1':
        s = 'map_' + seed[tek - 1] + '.txt'
        tek -= 1
        level_map = load_level(s)
        hx, hy, max_x, max_y = generate_level(level_map, f=1)
        heros.move(hx, hy)
    elif nam == '2':
        s = 'map_' + seed[tek + 1] + '.txt'
        tek += 1
        level_map = load_level(s)
        hx, hy, max_x, max_y = generate_level(level_map, f=2)
        heros.move(hx, hy)


def move(heros, movement=None):
    x, y = heros.pos
    newx, newy = x, y
    if movement == 'left':
        if x >= 0 and level_map[y][x - 1] != '#':
            newx, newy = x - 1, y
        elif x >= 0 and y - 1 >= 0 and level_map[y - 1][x - 1] != '#':
            newx, newy = x - 1, y - 1
    elif movement == 'right':
        if x <= max_x - 1 and level_map[y][x + 1] != '#':
            newx, newy = x + 1, y
        elif x <= max_x - 1 and y - 1 >= 0 and level_map[y - 1][x + 1] != '#':
            newx, newy = x + 1, y - 1
    elif movement is None:
        if y < max_y - 1 and level_map[y + 1][x] != '#':
            newx, newy = x, y + 1
    heros.move(newx, newy)
    new_lvl(newx, newy, heros)


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()
    sprite_group = pygame.sprite.Group()
    hero_group = pygame.sprite.Group()
    tile_images = {
        'dor': pygame.transform.scale(load_image('box.png'), (50, 50)),
        # 'empty': pygame.transform.scale(load_image('grass.png'), (50, 50)),
        'wall': pygame.transform.scale(load_image('kodred.png'), (50, 50))
    }
    player_image = pygame.transform.scale(load_image('Index_var2.png'), (21, 45))
    tile_width = tile_height = 50
    pygame.init()
    pygame.display.set_caption('Хз')
    size = width, height = 1500, 1000
    FPS = 50
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
    ticks, speed = 0, 5
    fon = load_image('fon.jpg')
    # fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    while running:
        keys = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.blit(fon, (0, 0))
        if ticks == speed:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                move(hero, 'left')
            elif keys[pygame.K_RIGHT]:
                move(hero, 'right')
            move(hero)
            ticks = 0

        ticks += 1
        all_sprites.draw(screen)
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
