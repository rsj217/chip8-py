import sys
import time

import pygame


def main():
    pygame.init()
    pygame.display.set_caption("Hello World")
    canvas = pygame.display.set_mode((640, 300))
    canvas.fill((0x00, 0x00, 0x00))
    pygame.display.update()

    while True:

        for x in range(0,100, 10):
            canvas.fill((0x00, 0x00, 0x00))
            pygame.draw.rect(
                canvas,
                (0xff, 0xff, 0xff),
                (x, 50, 10, 10),
                0
            )
            pygame.display.update()
            time.sleep(0.2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                print(f"event.type={event.type} event.key={event.key}")
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    main()
