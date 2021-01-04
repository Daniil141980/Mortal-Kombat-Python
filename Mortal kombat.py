import pygame
import sys
import os

pygame.init()
FPS = 60
WIDTH, HEIGHT = 765, 475
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_sprites = pygame.sprite.Group()
fighters_sprites = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    if not os.path.isfile(fullname):
        print(f'File {fullname} not found')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class Button(pygame.sprite.Sprite):
    def __init__(self, font, line, y, x, function):
        super().__init__(btn_sprites)
        self.color = pygame.Color(0, 0, 0)
        self.hsv = self.color.hsva
        self.color.hsva = (0, 100, 0, self.hsv[3])
        self.line = line
        self.font = font
        self.string_rendered = font.render(line, True, pygame.Color('red'), self.color)
        self.intro_rect = self.string_rendered.get_rect()
        self.intro_rect.top = y
        self.intro_rect.x = x
        self.rect = pygame.Rect(self.intro_rect[0],
                                self.intro_rect[1],
                                self.intro_rect[2],
                                self.intro_rect[3])
        self.image = pygame.Surface((self.intro_rect[2], self.intro_rect[3]), pygame.SRCALPHA, 32)
        self.image.blit(self.string_rendered, (0, 0))
        screen.blit(self.image, self.intro_rect)
        self.function = function

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(args[0].pos):
                self.color.hsva = (0, 100, 40, self.hsv[3])
            else:
                self.color.hsva = (0, 100, 0, self.hsv[3])
            if args[-1] == 'fatal' and self.function == 'back':
                self.string_rendered = self.font.render(self.line, True, pygame.Color('red'),
                                                        self.color)
                self.image.blit(self.string_rendered, (0, 0))
                screen.blit(self.image, self.intro_rect)
            elif args[-1] == 'start' and self.function in ['ii', 'two', 'fatality']:
                self.string_rendered = self.font.render(self.line, True, pygame.Color('red'),
                                                        self.color)
                self.image.blit(self.string_rendered, (0, 0))
                screen.blit(self.image, self.intro_rect)
            elif args[-1] == 'fight' and self.function in ['back', 'Китана', 'Горо',
                                                           'Скорпион', 'Скарлет', 'Саб-зиро', 'Шао-кан']:
                self.string_rendered = self.font.render(self.line, True, pygame.Color('red'),
                                                        self.color)
                self.image.blit(self.string_rendered, (0, 0))
                screen.blit(self.image, self.intro_rect)
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and args[0].button == 1 and \
                self.rect.collidepoint(args[0].pos):
            if self.function == 'ii':
                screen.fill(pygame.Color('black'))
                choice_fighters_screen()
            elif self.function == 'two':
                screen.fill(pygame.Color('black'))
                choice_fighters_screen()
            elif self.function == 'fatality':
                screen.fill(pygame.Color('black'))
                fatality_screen()
            elif self.function == 'back':
                screen.fill(pygame.Color('black'))
                start_screen()


def start_screen():
    intro_text = [("Играть с ИИ", 300, 'ii'),
                  ("Два игрока", 305, 'two'),
                  ("Список фаталити", 265, 'fatality')]
    fon = pygame.transform.scale(load_image('Menu_backround.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 170
    for line in intro_text:
        Button(font, line[0], text_coord, line[1], line[2])
        text_coord += 45
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event, 'start')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event, 'start')
        pygame.display.flip()
        clock.tick(FPS)


def fatality_screen():
    fon = pygame.transform.scale(load_image('Fatalities_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    run = True
    font = pygame.font.Font(None, 40)
    text_coord = 440
    Button(font, 'Назад', text_coord, 10, 'back')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event, 'fatal')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event, 'fatal')
        pygame.display.flip()
        clock.tick(FPS)


class ChoiceFighter(pygame.sprite.Sprite):
    def __init__(self, fighter, coord):
        super().__init__(fighters_sprites)
        self.image_fighter = pygame.transform.scale(load_image(fighter), (150, 130))
        self.image = self.image_fighter
        self.rect = self.image_fighter.get_rect()

        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            pass


def choice_fighters_screen():
    list_fighters = [('Kitana_unfas.jpeg', (210, 0), 'Китана'),
                     ('Goro_unfas.jpg', (210, 155), 'Горо'),
                     ('Scarlet_unfas.jpg', (210, 310), 'Скарлет'),
                     ('Scorpion_unfas.jpg', (380, 0), 'Скорпион'),
                     ('Shao_kan_unfas.jpg', (380, 155), 'Шао-кан'),
                     ('Sub-zero_unfas.jpg', (380, 310), 'Саб-зиро')]
    fon = pygame.transform.scale(load_image('Choice_fighter.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    run = True
    font = pygame.font.Font(None, 35)
    for fighter in list_fighters:
        ChoiceFighter(fighter[0], fighter[1])
        Button(font, fighter[-1], fighter[1][1] + 130, fighter[1][0], fighter[-1])
    fighters_sprites.draw(screen)
    font = pygame.font.Font(None, 40)
    text_coord = 440
    Button(font, 'Назад', text_coord, 10, 'back')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event, 'fight')
                fighters_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event, 'fight')
                fighters_sprites.update(event)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
