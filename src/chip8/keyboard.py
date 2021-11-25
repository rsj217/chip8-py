"""
::

        Keyboard                    Chip-8
    +---+---+---+---+           +---+---+---+---+
    | 1 | 2 | 3 | 4 |           | 1 | 2 | 3 | C |
    +---+---+---+---+           +---+---+---+---+
    | Q | W | E | R |           | 4 | 5 | 6 | D |
    +---+---+---+---+     =>    +---+---+---+---+
    | A | S | D | F |           | 7 | 8 | 9 | E |
    +---+---+---+---+           +---+---+---+---+
    | Z | X | C | V |           | A | 0 | B | F |
    +---+---+---+---+           +---+---+---+---+

"""


import sys
import pygame

from typing import List

_KEYS = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}


class Keyboard:

    def poll_event(self, keys_pressed_buf: List[int]):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.key_press(event, keys_pressed_buf)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def key_press(self, event, keys_pressed_buf: List[int]):

        if event.key in _KEYS:
            key = _KEYS[event.key]
            if event.type == pygame.KEYDOWN:
                keys_pressed_buf[key] = 1
            elif event.type == pygame.KEYUP:
                keys_pressed_buf[key] = 0
