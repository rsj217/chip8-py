

import pygame


def main():

    pygame.init()
    pygame.display.set_caption("Hello World")
    canvas = pygame.display.set_mode((640, 300))
    canvas.fill((0x00, 0x00, 0x00))
    pygame.display.update()

    while True:
        pass


if __name__ == '__main__':
    main()