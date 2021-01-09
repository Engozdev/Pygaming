import os
import sys
import pygame


def show_task(image_path, question, correct_answer):
    pygame.init()
    size = width, height = 1280, 960
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image('Terminal.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Arial', 30)
    quest = font.render(question, False, (255, 255, 255))
    screen.blit(quest, (250, 230))

    all_sprites = pygame.sprite.Group()
    task = pygame.sprite.Sprite()
    task.image = load_image(image_path)
    task.rect = 750, 150
    all_sprites.add(task)

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    ans = ''
    corr_flag = False
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                if event.key == 13:
                    if ans == correct_answer:
                        # ans = ''
                        pygame.draw.circle(screen, pygame.Color('green'), (1000, 700), 100)
                        corr_flag = True
                    else:
                        corr_flag = False
                        pygame.draw.circle(screen, pygame.Color('red'), (1000, 700), 100)
                elif event.key == 8:
                    ans = ans[:-1]
                    screen.blit(fon, (0, 0))
                    all_sprites.draw(screen)
                    if corr_flag:
                        pygame.draw.circle(screen, pygame.Color('green'), (1000, 700), 100)
                    else:
                        pygame.draw.circle(screen, pygame.Color('red'), (1000, 700), 100)
                    screen.blit(quest, (250, 230))
                else:
                    try:
                        ans += alphabet[event.key - 97]
                    except Exception:
                        pass
        all_sprites.draw(screen)
        display_ans = font.render(ans, False, (255, 255, 255))
        screen.blit(display_ans, (300, 650))
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


show_task("nepal.png", 'Which country has this flag?', 'nepal')
