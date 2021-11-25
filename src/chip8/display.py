from typing import List
import pygame
from src.chip8.conf import TITLE, SCREEN_HEIGHT, SCREEN_WIDTH, ZOOM, BG_COLOR, FG_COLOR


class Display:
    """
    +--------------------------+
    |(0, 0)             (63, 0)|
    |                          |
    |                          |
    |                          |
    |(0, 31)            (63,31)|
    +--------------------------+
    """

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH * ZOOM, SCREEN_HEIGHT * ZOOM))
        self.canvas.fill(BG_COLOR)
        pygame.display.update()

    def render(self, screen_buf: List[List[int]]):
        self.draw_frame(screen_buf)
        pygame.display.update()

    def draw_frame(self, screen_buf: List[List[int]]):
        self.canvas.fill(BG_COLOR)
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                if screen_buf[y][x] == 1:
                    self.draw_pixel(x, y)

    def draw_pixel(self, x: int, y: int):
        pygame.draw.rect(
            self.canvas,
            FG_COLOR,
            (x * ZOOM, y * ZOOM, ZOOM, ZOOM),
            0
        )

    def quit(self):
        pygame.quit()
