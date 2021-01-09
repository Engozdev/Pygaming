import os
import sys
import pygame


def show_task():
    pygame.init()
    size = width, height = 1280, 960
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('Terminal.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    all_sprites = pygame.sprite.Group()
    task = pygame.sprite.Sprite()
    task.image = load_image("nepal.png")
    task.rect = 800, 150

    all_sprites.add(task)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ans = ''

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                ans += alphabet[event.key - 97]
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


show_task()
