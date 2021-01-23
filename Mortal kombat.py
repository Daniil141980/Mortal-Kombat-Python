import pygame
import sys
import os
from random import choice
from threading import Timer

pygame.init()
pygame.mixer.init()
FPS = 60
WIDTH, HEIGHT = 765, 475
FON = ['', False]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
GRAVITY = 0.5

btn_sprites = pygame.sprite.Group()
something_image = pygame.sprite.Group()
fighters_sprite = pygame.sprite.Group()
animated_sprites = pygame.sprite.Group()
health_sprites = pygame.sprite.Group()
fight_animation = pygame.sprite.Group()
fight_animation_player1 = pygame.sprite.Group()
fight_animation_player2 = pygame.sprite.Group()
blood_sprites = pygame.sprite.Group()

TEST1 = ''
TEST2 = ''
PLAYER1 = ['', False]
PLAYER2 = ['', False]

HP_1 = 100
HP_2 = 100

menu_music = pygame.mixer.Sound('music_and_sounds/main_theme.mp3')
music1 = pygame.mixer.Sound("music_and_sounds/Mortal Kombat - Jade's Theme.mp3")
pygame.mixer.Sound.set_volume(music1, 0.01)
music2 = pygame.mixer.Sound("music_and_sounds/Mortal Kombat - 8 Bit.mp3")
pygame.mixer.Sound.set_volume(music2, 0.01)
music3 = pygame.mixer.Sound("music_and_sounds/toshiro-masuda-glued-state.mp3")
pygame.mixer.Sound.set_volume(music3, 0.01)

click_sound = pygame.mixer.Sound('music_and_sounds/click_sound.mp3')
hit_sound1 = pygame.mixer.Sound('music_and_sounds/kick1.mp3')
hit_sound2 = pygame.mixer.Sound('music_and_sounds/kick2.mp3')

pygame.mixer.Sound.set_volume(menu_music, 0.01)
pygame.mixer.Sound.play(menu_music, loops=99)


def timeover():
    global HP_1
    global HP_2
    if HP_1 >= HP_2:
        HP_2 = 0
    elif HP_2 > HP_1:
        HP_1 = 0


fight_timer = Timer(60, timeover)


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

dict_fighters_walk = {'Скорпион': (load_image('Scorpion_walk.png'), 9, 1),
                      'Горо': (load_image('Goro_walk.png'), 9, 1),
                      'Китана': (load_image('Kitana_walk.png', colorkey=-1), 8, 1),
                      'Шао-кан': (load_image('Shao_walk.png'), 8, 1, -10, 100),
                      'Саб-зиро': (load_image('Sub_walk.png', colorkey=-1), 9, 1),
                      'Рейден': (load_image('Raiden_walk.png', colorkey=-1), 8, 1)}

dict_fighters_blok = {'Скорпион': load_image('Scorpion_blok.png'),
                      'Горо': load_image('Goro_blok.png'),
                      'Китана': load_image('Kitana_blok.png', colorkey=-1),
                      'Шао-кан': load_image('Shao_blok.png'),
                      'Саб-зиро': load_image('Sub_blok.png', colorkey=-1),
                      'Рейден': load_image('Raiden_blok.png', colorkey=-1)}

dict_fighters_end = {'Скорпион': load_image('Scorpion_end.png'),
                     'Горо': load_image('Goro_end.png'),
                     'Китана': load_image('Kitana_end.png', colorkey=-1),
                     'Шао-кан': load_image('Shao_end.png'),
                     'Саб-зиро': load_image('Sub_end.png', colorkey=-1),
                     'Рейден': load_image('Raiden_end.png', colorkey=-1)}

dict_fighters_sit_down = {'Скорпион': load_image('Scorpion_sit_down.png'),
                          'Горо': load_image('Goro_sit_down.png'),
                          'Китана': load_image('Kitana_sit_down.png', colorkey=-1),
                          'Шао-кан': load_image('Shao_sit_down.png'),
                          'Саб-зиро': load_image('Sub_sit_down.png', colorkey=-1),
                          'Рейден': load_image('Raiden_sit_down.png', colorkey=-1)}

dict_fighters_hit_hand = {'Скорпион': (load_image('Scorpion_hit_1.png'),
                                       load_image('Scorpion_hit_2.png'), 3),
                          'Горо': (load_image('Goro_hit_1.png'),
                                   load_image('Goro_hit_1.png'), 5),
                          'Китана': (load_image('Kitana_hit_1.png', colorkey=-1),
                                     load_image('Kitana_hit_2.png', colorkey=-1), 3),
                          'Шао-кан': (load_image('Shao_hit_1.png'),
                                      load_image('Shao_hit_2.png'), 3),
                          'Саб-зиро': (load_image('Sub_hit_1.png', colorkey=-1),
                                       load_image('Sub_hit_2.png', colorkey=-1), 3),
                          'Рейден': (load_image('Raiden_hit_1.png', colorkey=-1),
                                     load_image('Raiden_hit_2.png', colorkey=-1), 3)}

dict_fighters_hitting = {'Скорпион': load_image('Scorpion_hitting.png'),
                         'Горо': load_image('Goro_hitting.png'),
                         'Китана': load_image('Kitana_hitting.png', colorkey=-1),
                         'Шао-кан': load_image('Shao_hitting.png'),
                         'Саб-зиро': load_image('Sub_hitting.png', colorkey=-1),
                         'Рейден': load_image('Raiden_hitting.png', colorkey=-1)}

dict_fighters_dead = {'Скорпион': (load_image('Scorpion_dead.png'), 5),
                      'Горо': (load_image('Goro_dead.png'), 3),
                      'Китана': (load_image('Kitana_dead.png', colorkey=-1), 5),
                      'Шао-кан': (load_image('Shao_dead.png'), 2),
                      'Саб-зиро': (load_image('Sub_dead.png', colorkey=-1), 5),
                      'Рейден': (load_image('Raiden_dead.png', colorkey=-1), 5)}

dict_fighters_win = {'Скорпион': (load_image('Scorpion_win.png'), 2),
                     'Горо': (load_image('Goro_win.png'), 3),
                     'Китана': (load_image('Kitana_win.png', colorkey=-1), 3),
                     'Шао-кан': (load_image('Shao_win.png'), 2),
                     'Саб-зиро': (load_image('Sub_win.png', colorkey=-1), 2),
                     'Рейден': (load_image('Raiden_win.png', colorkey=-1), 2)}

dict_fighters_hit_leg = {'Скорпион': (load_image('Scorpion_hit_leg.png'), 2),
                         'Горо': (load_image('Goro_hit_leg.png'), 3),
                         'Китана': (load_image('Kitana_hit_leg.png', colorkey=-1), 2),
                         'Шао-кан': (load_image('Shao_hit_leg.png'), 2),
                         'Саб-зиро': (load_image('Sub_hit_leg.png', colorkey=-1), 2),
                         'Рейден': (load_image('Raiden_hit_leg.png', colorkey=-1), 2)}


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
            if self.function == 'two':
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
            elif self.function == 'start':
                del_sprite(btn_sprites.sprites())
                del_sprite(animated_sprites.sprites())
                del_sprite(something_image.sprites())
                fight_screen()


def del_sprite(sprites):
    for sprite in sprites:
        sprite.kill()


def start_screen():
    intro_text = [("Играть", 330, 'two'),
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
    list_fighters = [('Kitana_unfas.jpg', (210, 0), 'FGH'),
                     ('Goro_unfas.jpg', (210, 155), 'GHF'),
                     ('Raiden_unfas.jpg', (210, 310), 'GFH'),
                     ('Scorpion_unfas.jpg', (380, 0), 'FHG'),
                     ('Shao_kan_unfas.jpg', (380, 155), 'HGF'),
                     ('Sub-zero_unfas.jpg', (380, 310), 'HFG')]
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
        if self.count % 9 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.which == 2:
                image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = pygame.transform.scale(self.frames[self.cur_frame], (175, 225))
        self.count += 1


def choice_fighters_screen():
    list_fighters = [('Kitana_unfas.jpg', (210, 0), 'Китана'),
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


dict_unfas = {'Скорпион': 'Scorpion',
              'Горо': 'Goro',
              'Китана': 'Kitana',
              'Шао-кан': 'Shao_kan',
              'Саб-зиро': 'Sub-zero',
              'Рейден': 'Raiden'}


class HealthFighter(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, player):
        super().__init__(health_sprites)
        self.player = player
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
        pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, width, height))
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        if self.player == 1:
            if HP_1 >= 0:
                width = int(self.width / 100 * HP_1)
                self.image = pygame.Surface((width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, width, self.height))
                self.rect = pygame.Rect(self.x, self.y, width, self.height)
            else:
                width = 0
                self.image = pygame.Surface((width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, width, self.height))
                self.rect = pygame.Rect(self.x, self.y, width, self.height)
        elif self.player == 2:
            if HP_2 >= 0:
                width = int(self.width / 100 * HP_2)
                self.image = pygame.Surface((width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, width, self.height))
                self.rect = pygame.Rect(self.x, self.y, width, self.height)
            else:
                width = 0
                self.image = pygame.Surface((width, self.height), pygame.SRCALPHA, 32)
                pygame.draw.rect(self.image, pygame.Color("green"), (0, 0, width, self.height))
                self.rect = pygame.Rect(self.x, self.y, width, self.height)


class Field:
    def __init__(self):
        self.field = [[0] * 17 for _ in range(5)]
        self.width = 17
        self.height = 5
        self.left = 0
        self.top = 55
        self.cell_size = 45
        self.x_pos_1 = 0
        self.y_pos_1 = 4
        self.x_pos_2 = 14
        self.y_pos_2 = 4

    def change_pos(self, where, who):
        if where == 'left':
            if self.x_pos_1 > 0 and who == 1 and \
                    ((self.x_pos_2 > self.x_pos_1) or
                     ((self.x_pos_1 - self.x_pos_2) > 2)):
                self.x_pos_1 -= 1
            elif self.x_pos_2 > 0 and who == 2 and \
                    ((self.x_pos_1 > self.x_pos_2) or
                     ((self.x_pos_2 - self.x_pos_1) > 2)):
                self.x_pos_2 -= 1
        elif where == 'right':
            if self.x_pos_1 < self.width - 3 and who == 1 and \
                    ((self.x_pos_1 > self.x_pos_2) or
                     ((self.x_pos_2 - self.x_pos_1) > 2)):
                self.x_pos_1 += 1
            elif self.x_pos_2 < self.width - 3 and who == 2 and \
                    ((self.x_pos_2 > self.x_pos_1) or
                     ((self.x_pos_1 - self.x_pos_2) > 2)):
                self.x_pos_2 += 1

    def near(self):
        if abs(self.x_pos_1 - self.x_pos_2) == 2 and \
                self.y_pos_1 == self.y_pos_2:
            return True
        return False


class AnimationForFight(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, player):
        super().__init__(fight_animation)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.player = player
        if player == 2:
            self.image = pygame.transform.flip(
                pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
        else:
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
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

    def update(self, change):
        if change[0] is True:
            self.rect = self.rect.move(change[1], change[2])
        if change[1] == 'end':
            if self.count % 20 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.player == 2:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
                else:
                    self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
        elif change[1] == 'block':
            if self.count % 35 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.player == 2:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
                else:
                    self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
        elif change[1] == 'hit':
            if self.count % 10 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.player == 2:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
                else:
                    self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
        elif change[1] == 'hitting':
            if self.count % 10 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                if self.player == 2:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
                else:
                    self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
        elif self.count % 9 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            if self.player == 2:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(self.frames[self.cur_frame], (135, 210)), True, False)
            else:
                self.image = pygame.transform.scale(self.frames[self.cur_frame], (135, 210))
        self.count += 1


def draw_icon():
    size = (250, 20)
    screen.blit(pygame.transform.scale(load_image(dict_unfas[PLAYER1[0]] + '_unfas.jpg'),
                                       (80, 90)), (0, 0))
    screen.blit(pygame.transform.scale(load_image(dict_unfas[PLAYER2[0]] + '_unfas.jpg'),
                                       (80, 90)), (WIDTH - 80, 0))
    screen.blit(pygame.transform.scale(load_image('health_line.jpg'), size), (90, 10))
    screen.blit(pygame.transform.scale(load_image('health_line.jpg'), size), (WIDTH - 340, 10))


class Blood(pygame.sprite.Sprite):
    blood_png = [pygame.transform.scale(load_image('blood.png'), (9, 9))]
    for scale in (6, 7, 8, 9, 10):
        blood_png.append(pygame.transform.scale(blood_png[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(blood_sprites)
        self.image = choice(self.blood_png)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, WIDTH, HEIGHT)):
            self.kill()


def blood(x, y):
    particle_count = 30
    numbers = range(-2, 3)
    for _ in range(particle_count):
        Blood((x, y), choice(numbers), choice(numbers))


def fight_screen():
    fight_timer.start()
    music_randomizer = choice([1, 2, 3])
    pygame.mixer.Sound.stop(menu_music)
    if music_randomizer == 1:
        pygame.mixer.Sound.play(music1, loops=99)
    elif music_randomizer == 2:
        pygame.mixer.Sound.play(music2, loops=99)
    else:
        pygame.mixer.Sound.play(music3, loops=99)
    global HP_1, HP_2
    fon = pygame.transform.scale(load_image(FON[0]), (WIDTH, HEIGHT))
    draw_icon()
    screen.blit(fon, (0, 0))
    for i in [(96, 14, 239, 13, 1), (WIDTH - 334, 14, 239, 13, 2)]:
        HealthFighter(i[0], i[1], i[2], i[3], i[4])
    run = True
    field = Field()
    speed = 2.5
    x_pos_1 = field.x_pos_1
    y_pos_1 = field.y_pos_1
    x_pos_2 = field.x_pos_2
    y_pos_2 = field.y_pos_2
    count1 = 0
    count2 = 0
    fight_animation_player1.add(AnimationForFight(dict_fighters[PLAYER1[0]][0],
                                                  dict_fighters[PLAYER1[0]][1],
                                                  dict_fighters[PLAYER1[0]][2],
                                                  x_pos_1 * field.cell_size,
                                                  y_pos_1 * field.cell_size + field.top, 1))
    fight_animation_player2.add(AnimationForFight(dict_fighters[PLAYER2[0]][0],
                                                  dict_fighters[PLAYER2[0]][1],
                                                  dict_fighters[PLAYER2[0]][2],
                                                  x_pos_2 * field.cell_size,
                                                  y_pos_2 * field.cell_size + field.top, 2))
    flag_static_1 = False
    flag_static_2 = False
    flag_block_1 = False
    flag_block_2 = False
    flag_sit_1 = False
    flag_sit_2 = False
    flag_hit_hand_1 = False
    flag_hit_hand_2 = False
    flag_hit_leg_1 = False
    flag_hit_leg_2 = False
    flag_hitting_1 = False
    flag_hitting_2 = False
    flag_end_1 = False
    flag_end_2 = False
    flag_win_1 = False
    flag_win_2 = False
    hit_count_moves_1 = 0
    hit_count_moves_2 = 0
    hit_count_moves_leg_1 = 0
    hit_count_moves_leg_2 = 0
    if PLAYER1[0] == 'Горо':
        count_hit_leg_1 = 3
    else:
        count_hit_leg_1 = 2
    if PLAYER2[0] == 'Горо':
        count_hit_leg_2 = 3
    else:
        count_hit_leg_2 = 2
    hitting_count_1 = 0
    hitting_count_2 = 0
    count_end_hitting_1 = 2
    count_end_hitting_2 = 2
    if PLAYER1[0] == 'Горо':
        count_hit_hand_1 = 4
    else:
        count_hit_hand_1 = 3
    if PLAYER2[0] == 'Горо':
        count_hit_hand_2 = 4
    else:
        count_hit_hand_2 = 3
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                flag_sit_2 = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                flag_sit_2 = False
            if key[pygame.K_s]:
                flag_sit_1 = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_s:
                flag_sit_1 = False
            if key[pygame.K_RIGHT]:
                field.change_pos('right', 2)
            elif key[pygame.K_LEFT]:
                field.change_pos('left', 2)
            if key[pygame.K_d]:
                field.change_pos('right', 1)
            elif key[pygame.K_a]:
                field.change_pos('left', 1)
            if key[pygame.K_x]:
                flag_hit_hand_1 = True
            elif key[pygame.K_c]:
                flag_hit_leg_1 = True
            elif key[pygame.K_v]:
                flag_block_1 = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_v:
                flag_block_1 = False
            if key[pygame.K_i]:
                flag_hit_hand_2 = True
            elif key[pygame.K_o]:
                flag_hit_leg_2 = True
            elif key[pygame.K_p]:
                flag_block_2 = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_p:
                flag_block_2 = False
        screen.blit(fon, (0, 0))
        draw_icon()
        btn_sprites.draw(screen)
        health_sprites.update()
        health_sprites.draw(screen)
        if flag_win_1:
            if flag_static_1 != 'win':
                flag_static_1 = 'win'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_win[PLAYER1[0]][0],
                                                              dict_fighters_win[PLAYER1[0]][1],
                                                              1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'block', 0))
        elif flag_end_1:
            if flag_static_1 != 'die':
                flag_win_2 = True
                flag_static_1 = 'die'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_end[PLAYER1[0]],
                                                              2, 1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'block', 0))
        elif HP_1 <= 0:
            if flag_static_1 != 'end':
                flag_static_1 = 'end'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_dead[PLAYER1[0]][0],
                                                              dict_fighters_dead[PLAYER1[0]][1],
                                                              1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'end', 0))
        elif flag_hitting_1:
#            kick_sound_randomizer = choice([1, 2])
#            if kick_sound_randomizer == 1:
#                pygame.mixer.Sound.play(hit_sound1)
#            else:
 #               pygame.mixer.Sound.play(hit_sound2)
            if flag_static_1 != 'hitting':
                flag_static_1 = 'hitting'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_hitting[PLAYER1[0]],
                                                              2, 1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'hitting', 0))
            if hitting_count_1 % 10 == 0:
                count_end_hitting_1 -= 1
            if count_end_hitting_1 == 0:
                blood(x_pos_1 * field.cell_size + field.cell_size // 2,
                      y_pos_1 * field.cell_size + field.top + field.cell_size // 2)
                flag_hitting_1 = False
                count_end_hitting_1 = 1
            hitting_count_1 += 1
        elif flag_hit_hand_1:
            if flag_static_1 != 'hit_hand':
                flag_static_1 = 'hit_hand'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(choice(dict_fighters_hit_hand[PLAYER1[0]][:2]),
                                                              dict_fighters_hit_hand[PLAYER1[0]][2],
                                                              1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'hit', 0))
            if hit_count_moves_1 % 10 == 0:
                count_hit_hand_1 -= 1
            if count_hit_hand_1 == 0:
                if field.near():
                    if HP_2 <= 0:
                        flag_end_2 = True
                    elif flag_sit_2:
                        pass
                    elif flag_block_2 is False:
                        flag_hitting_2 = True
                        HP_2 -= 10
                    else:
                        HP_2 -= 5

                flag_hit_hand_1 = False
                pygame.mixer.Sound.play(hit_sound1)
                if PLAYER1[0] == 'Горо':
                    count_hit_hand_1 = 4
                else:
                    count_hit_hand_1 = 3
            hit_count_moves_1 += 1
        elif flag_hit_leg_1:
            if flag_static_1 != 'hit_leg':
                flag_static_1 = 'hit_leg'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_hit_leg[PLAYER1[0]][0],
                                                              dict_fighters_hit_leg[PLAYER1[0]][1],
                                                              1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'hit', 0))
            if hit_count_moves_leg_1 % 10 == 0:
                count_hit_leg_1 -= 1
            if count_hit_leg_1 == 0:
                if field.near():
                    if HP_2 <= 0:
                        flag_end_2 = True
                    elif flag_sit_2:
                        pass
                    elif flag_block_2 is False:
                        flag_hitting_2 = True
                        HP_2 -= 15
                    else:
                        HP_2 -= 5

                flag_hit_leg_1 = False
                pygame.mixer.Sound.play(hit_sound2)
                if PLAYER1[0] == 'Горо':
                    count_hit_leg_1 = 3
                else:
                    count_hit_leg_1 = 2
            hit_count_moves_leg_1 += 1
        elif flag_block_1:
            if flag_static_1 != 'block':
                flag_static_1 = 'block'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_blok[PLAYER1[0]],
                                                              2, 1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'block', 0))
        elif flag_sit_1:
            if flag_static_1 != 'sit':
                flag_static_1 = 'sit'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_sit_down[PLAYER1[0]],
                                                              2, 1, x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            fight_animation_player1.draw(screen)
            fight_animation_player1.update((False, 'block', 0))
        elif x_pos_1 != field.x_pos_1:
            if flag_static_1 != 'move':
                flag_static_1 = 'move'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters_walk[PLAYER1[0]][0],
                                                              dict_fighters_walk[PLAYER1[0]][1],
                                                              dict_fighters_walk[PLAYER1[0]][2],
                                                              x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size
                                                              + field.top, 1))
            if x_pos_1 < field.x_pos_1:
                count1 += speed
                fight_animation_player1.draw(screen)
                fight_animation_player1.update((True, speed,
                                                0))
                if abs(count1) % 45 == 0:
                    count1 = 0
                    x_pos_1 += 1
            elif x_pos_1 > field.x_pos_1:
                count1 -= speed
                fight_animation_player1.draw(screen)
                fight_animation_player1.update((True, -speed,
                                                0))
                if abs(count1) % 45 == 0:
                    count1 = 0
                    x_pos_1 -= 1
        else:
            fight_animation_player1.draw(screen)
            if flag_static_1 != 'static':
                flag_static_1 = 'static'
                del_sprite(fight_animation_player1)
                fight_animation_player1.add(AnimationForFight(dict_fighters[PLAYER1[0]][0],
                                                              dict_fighters[PLAYER1[0]][1],
                                                              dict_fighters[PLAYER1[0]][2],
                                                              x_pos_1 * field.cell_size,
                                                              y_pos_1 * field.cell_size +
                                                              field.top, 1))
            fight_animation_player1.update((False, 0, 0))
        if flag_win_2:
            if flag_static_2 != 'win':
                flag_static_2 = 'win'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_win[PLAYER2[0]][0],
                                                              dict_fighters_win[PLAYER2[0]][1],
                                                              1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'block', 0))
        elif flag_end_2:
            if flag_static_2 != 'die':
                flag_win_1 = True
                flag_static_2 = 'die'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_end[PLAYER2[0]],
                                                              2, 1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'block', 0))
        elif HP_2 <= 0:
            if flag_static_2 != 'end':
                flag_static_2 = 'end'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_dead[PLAYER2[0]][0],
                                                              dict_fighters_dead[PLAYER2[0]][1],
                                                              1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'end', 0))
        elif flag_hitting_2:
            if flag_static_2 != 'hitting':
                flag_static_2 = 'hitting'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_hitting[PLAYER2[0]],
                                                              2, 1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'hitting', 0))
            if hitting_count_2 % 10 == 0:
                count_end_hitting_2 -= 1
            if count_end_hitting_2 == 0:
                blood(x_pos_2 * field.cell_size + field.cell_size // 2,
                      y_pos_2 * field.cell_size + field.top + field.cell_size // 2)
                flag_hitting_2 = False
                count_end_hitting_2 = 1
            hitting_count_2 += 1
        elif flag_hit_hand_2:
            if flag_static_2 != 'hit_hand':
                flag_static_2 = 'hit_hand'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(choice(dict_fighters_hit_hand[PLAYER2[0]][:2]),
                                                              dict_fighters_hit_hand[PLAYER2[0]][2],
                                                              1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'hit', 0))
            if hit_count_moves_2 % 10 == 0:
                count_hit_hand_2 -= 1
            if count_hit_hand_2 == 0:
                if field.near():
                    if HP_1 <= 0:
                        flag_end_1 = True
                    elif flag_sit_1:
                        pass
                    elif flag_block_1 is False:
                        flag_hitting_1 = True
                        HP_1 -= 10
                    else:
                        HP_1 -= 5

                flag_hit_hand_2 = False
                pygame.mixer.Sound.play(hit_sound1)
                if PLAYER2[0] == 'Горо':
                    count_hit_hand_2 = 4
                else:
                    count_hit_hand_2 = 3
            hit_count_moves_2 += 1
        elif flag_hit_leg_2:
            if flag_static_2 != 'hit_leg':
                flag_static_2 = 'hit_leg'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_hit_leg[PLAYER2[0]][0],
                                                              dict_fighters_hit_leg[PLAYER2[0]][1],
                                                              1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'hit', 0))
            if hit_count_moves_leg_2 % 10 == 0:
                count_hit_leg_2 -= 1
            if count_hit_leg_2 == 0:
                if field.near():
                    if HP_1 <= 0:
                        flag_end_1 = True
                    elif flag_sit_1:
                        pass
                    elif flag_block_1 is False:
                        flag_hitting_1 = True
                        HP_1 -= 15
                    else:
                        HP_1 -= 5

                flag_hit_leg_2 = False
                pygame.mixer.Sound.play(hit_sound2)
                if PLAYER2[0] == 'Горо':
                    count_hit_leg_2 = 3
                else:
                    count_hit_leg_2 = 2
            hit_count_moves_leg_2 += 1
        elif flag_block_2:
            if flag_static_2 != 'block':
                flag_static_2 = 'block'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_blok[PLAYER2[0]],
                                                              2, 1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'block', 0))
        elif flag_sit_2:
            if flag_static_2 != 'sit':
                flag_static_2 = 'sit'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_sit_down[PLAYER2[0]],
                                                              2, 1, x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            fight_animation_player2.draw(screen)
            fight_animation_player2.update((False, 'block', 0))
        elif x_pos_2 != field.x_pos_2:
            if flag_static_2 != 'move':
                flag_static_2 = 'move'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters_walk[PLAYER2[0]][0],
                                                              dict_fighters_walk[PLAYER2[0]][1],
                                                              dict_fighters_walk[PLAYER2[0]][2],
                                                              x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size
                                                              + field.top, 2))
            if x_pos_2 < field.x_pos_2:
                count2 += speed
                fight_animation_player2.draw(screen)
                fight_animation_player2.update((True, speed,
                                                0))
                if abs(count2) % 45 == 0:
                    count2 = 0
                    x_pos_2 += 1
            elif x_pos_2 > field.x_pos_2:
                count2 -= speed
                fight_animation_player2.draw(screen)
                fight_animation_player2.update((True, -speed,
                                                0))
                if abs(count2) % 45 == 0:
                    count2 = 0
                    x_pos_2 -= 1
        else:
            fight_animation_player2.draw(screen)
            if flag_static_2 != 'static':
                flag_static_2 = 'static'
                del_sprite(fight_animation_player2)
                fight_animation_player2.add(AnimationForFight(dict_fighters[PLAYER2[0]][0],
                                                              dict_fighters[PLAYER2[0]][1],
                                                              dict_fighters[PLAYER2[0]][2],
                                                              x_pos_2 * field.cell_size,
                                                              y_pos_2 * field.cell_size +
                                                              field.top, 2))
            fight_animation_player2.update((False, 0, 0))
        blood_sprites.update()
        blood_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
terminate()
