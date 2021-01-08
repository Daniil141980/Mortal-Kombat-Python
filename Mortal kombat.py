import pygame
import sys
import os

pygame.init()
pygame.mixer.init()
FPS = 60
WIDTH, HEIGHT = 765, 475
FON = ['', False]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

btn_sprites = pygame.sprite.Group()
something_image = pygame.sprite.Group()
fighters_sprite = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()

TEST1 = ''
TEST2 = ''
PLAYER1 = ['', False]
PLAYER2 = ['', False]

menu_music = pygame.mixer.Sound('music_and_sounds/main_theme.mp3')
click_sound = pygame.mixer.Sound('music_and_sounds/click_sound.mp3')
pygame.mixer.Sound.set_volume(menu_music, 0.01)
pygame.mixer.Sound.play(menu_music)


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


dict_fighters = {'Скорпион': (load_image('Scorpion_special.png'), 6, 1, -5, 100),
                 'Горо': (load_image('Goro_special.png'), 7, 1, -15, 100),
                 'Китана': (load_image('Kitana_special.png', colorkey=-1), 5, 1, 0, 100),
                 'Шао-кан': (load_image('Shao_special.png'), 6, 1, -10, 100),
                 'Саб-зиро': (load_image('Sub_special.png', colorkey=-1), 10, 1, 0, 100),
                 'Рейден': (load_image('Raiden_special.png', colorkey=-1), 8, 1, 0, 100)}


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
        self.intro_rect.y = y
        self.intro_rect.x = x
        self.rect = pygame.Rect(self.intro_rect[0],
                                self.intro_rect[1],
                                self.intro_rect[2],
                                self.intro_rect[3])
        self.image = self.string_rendered
        self.function = function

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(args[0].pos):
                self.color.hsva = (0, 100, 40, self.hsv[3])
            else:
                self.color.hsva = (0, 100, 0, self.hsv[3])
            self.string_rendered = self.font.render(self.line, True,
                                                    pygame.Color('red'),
                                                    self.color)
            self.image = self.string_rendered
        elif args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pygame.mixer.Sound.set_volume(click_sound, 0.5)
            pygame.mixer.Sound.play(click_sound)
            if self.function == 'ii':
                screen.fill(pygame.Color('black'))
                del_sprite(btn_sprites.sprites())
                choice_fighters_screen()
            elif self.function == 'two':
                screen.fill(pygame.Color('black'))
                del_sprite(btn_sprites.sprites())
                choice_fighters_screen()
            elif self.function == 'fatality':
                screen.fill(pygame.Color('black'))
                del_sprite(btn_sprites.sprites())
                fatality_screen()
            elif self.function == 'back':
                screen.fill(pygame.Color('black'))
                del_sprite(btn_sprites.sprites())
                del_sprite(something_image.sprites())
                del_sprite(fighters_sprite.sprites())
                del_sprite(animated_sprites.sprites())
                non_player_fon()
                start_screen()
            elif self in fighters_sprite:
                if PLAYER1[1] is True:
                    if PLAYER2[1] is not True:
                        PLAYER2[0] = self.function
                else:
                    PLAYER1[0] = self.function
            elif self.function == 'choice':
                if PLAYER1[1] is True:
                    if PLAYER2[0] != '':
                        PLAYER2[1] = True
                        self.line = 'Далее'
                        self.string_rendered = self.font.render(self.line,
                                                                True,
                                                                pygame.Color('red'),
                                                                self.color)
                        self.image = self.string_rendered
                        self.function = 'next'
                elif PLAYER1[0] != '':
                    PLAYER1[1] = True
            elif self.function == 'next':
                screen.fill(pygame.Color('black'))
                del_sprite(btn_sprites.sprites())
                del_sprite(something_image.sprites())
                del_sprite(fighters_sprite.sprites())
                del_sprite(animated_sprites.sprites())
                choice_fon_fighter()
            elif self.function == 'choice_fon':
                if FON[0] != '':
                    FON[1] = True
                    self.line = 'Старт'
                    self.string_rendered = self.font.render(self.line,
                                                            True,
                                                            pygame.Color('red'),
                                                            self.color)
                    self.image = self.string_rendered
                    self.function = 'start'


def del_sprite(sprites):
    for sprite in sprites:
        sprite.kill()


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
                btn_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event)
        btn_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def fatality_screen():
    list_fighters = [('Kitana_unfas.jpeg', (210, 0), 'Китана'),
                     ('Goro_unfas.jpg', (210, 155), 'Горо'),
                     ('Raiden_unfas.jpg', (210, 310), 'Рейден'),
                     ('Scorpion_unfas.jpg', (380, 0), 'Скорпион'),
                     ('Shao_kan_unfas.jpg', (380, 155), 'Шао-кан'),
                     ('Sub-zero_unfas.jpg', (380, 310), 'Саб-зиро')]
    fon = pygame.transform.scale(load_image('Fatalities_background.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 32)
    for fighter in list_fighters:
        SomethingImage(fighter[0], fighter[1], (150, 130))
        Button(font, fighter[-1], fighter[1][1] + 130, fighter[1][0], fighter[-1])
    something_image.draw(screen)
    run = True
    font = pygame.font.Font(None, 40)
    text_coord = 440
    Button(font, 'Назад', text_coord, 10, 'back')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event)
        btn_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def non_player_fon():
    global TEST1, TEST2, PLAYER1, PLAYER2, FON
    TEST1 = ''
    TEST2 = ''
    PLAYER1 = ['', False]
    PLAYER2 = ['', False]
    FON = ['', False]


class SomethingImage(pygame.sprite.Sprite):
    def __init__(self, image, coord, size):
        super().__init__(something_image)
        self.picture = image
        self.image_fighter = pygame.transform.scale(load_image(image), size)
        self.image = self.image_fighter
        self.rect = self.image_fighter.get_rect()
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    def update(self, *args):
        global FON
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            pygame.mixer.Sound.set_volume(click_sound, 0.5)
            pygame.mixer.Sound.play(click_sound)
            FON[0] = self.picture


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, which_player):
        global TEST1, TEST2
        super().__init__(animated_sprites)
        self.frames = []
        self.which = which_player
        if which_player == 1:
            self.player = PLAYER1[0]
            TEST1 = self.player
            x = dict_fighters[self.player][3]
            y = dict_fighters[self.player][4]
        else:
            self.player = PLAYER2[0]
            TEST2 = self.player
            x = WIDTH - dict_fighters[self.player][3] - 175
            y = dict_fighters[self.player][4]
        if len(animated_sprites.sprites()) > 1 and PLAYER1[1] is not True:
            for i in range(len(animated_sprites.sprites()) - 1):
                animated_sprites.sprites()[i].kill()
        elif len(animated_sprites.sprites()) > 2 and PLAYER1[1] is True and PLAYER2[1] is not True:
            for i in range(1, len(animated_sprites.sprites()) - 1):
                animated_sprites.sprites()[i].kill()
        sheet = dict_fighters[self.player][0]
        columns = dict_fighters[self.player][1]
        rows = dict_fighters[self.player][2]
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        if which_player == 2:
            image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
            self.image = pygame.transform.flip(image, True, False)
        else:
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
        self.rect = self.rect.move(x, y)
        self.count = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))
        for j in range(rows - 1, -1, -1):
            for i in range(columns - 2, 0, -1):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.count % 11 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.which == 2:
                image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
        self.count += 1


def choice_fighters_screen():
    list_fighters = [('Kitana_unfas.jpeg', (210, 0), 'Китана'),
                     ('Goro_unfas.jpg', (210, 155), 'Горо'),
                     ('Raiden_unfas.jpg', (210, 310), 'Рейден'),
                     ('Scorpion_unfas.jpg', (380, 0), 'Скорпион'),
                     ('Shao_kan_unfas.jpg', (380, 155), 'Шао-кан'),
                     ('Sub-zero_unfas.jpg', (380, 310), 'Саб-зиро')]
    fon = pygame.transform.scale(load_image('Choice_fighter.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    run = True
    font = pygame.font.Font(None, 35)
    for fighter in list_fighters:
        SomethingImage(fighter[0], fighter[1], (150, 130))
        fighters_sprite.add(Button(font, fighter[-1], fighter[1][1] + 130,
                                   fighter[1][0], fighter[-1]))
    something_image.draw(screen)
    font = pygame.font.Font(None, 40)
    text_coord = 440
    Button(font, 'Назад', text_coord, 10, 'back')
    Button(font, 'Выбрать', text_coord, 640, 'choice')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event)
        if PLAYER1[1] is True and PLAYER2[1] is True:
            animated_sprites.update()
        elif PLAYER1[1] is True and PLAYER2[1] is not True:
            if PLAYER2[0] == TEST2:
                animated_sprites.update()
            else:
                AnimatedSprite(2)
        elif PLAYER1[1] is not True and PLAYER1[0] != '':
            if PLAYER1[0] == TEST1:
                animated_sprites.update()
            else:
                AnimatedSprite(1)
        screen.blit(fon, (0, 0))
        btn_sprites.draw(screen)
        something_image.draw(screen)
        animated_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def choice_fon_fighter():
    list_fon = [('Choice_fon1.jpg', (30.6, 330)),
                ('Choice_fon2.jpg', (214.2, 330)),
                ('Choice_fon3.jpg', (397.8, 330)),
                ('Choice_fon4.jpg', (581.4, 330)),
                ('Choice_fon5.png', (30.6, 220)),
                ('Choice_fon6.jpg', (214.2, 220)),
                ('Choice_fon7.png', (397.8, 220)),
                ('Choice_fon8.jpg', (581.4, 220))]
    fon = pygame.transform.scale(load_image('Choice_fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    run = True
    for fighter in list_fon:
        SomethingImage(fighter[0], fighter[1], (153, 95))
    something_image.draw(screen)
    font = pygame.font.Font(None, 40)
    text_coord = 440
    Button(font, 'Назад', text_coord, 10, 'back')
    Button(font, 'Выбрать', text_coord, 640, 'choice_fon')
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                btn_sprites.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                btn_sprites.update(event)
                if FON[1] is False:
                    something_image.update(event)
        if FON[0] != '':
            fon = pygame.transform.scale(load_image(FON[0]), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        btn_sprites.draw(screen)
        something_image.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
