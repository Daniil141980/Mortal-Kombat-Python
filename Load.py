import pygame
import sys
import os

pygame.init()


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
