import pygame

ZOOM = 10
SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32

BG_COLOR = (0xa0, 0xe6, 0xfa)
FG_COLOR = (0xff, 0xff, 0xff)
START_ADDR = 0x200
_MEM_SIZE = 4 * 1024
_FONTSET = [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80]  # F


class Memory:

    def __init__(self):
        # 4KB memory
        self._ram = [0] * 4 * 1024
        # stack
        self._stack = []
        for i in range(len(_FONTSET)):
            self._ram[i] = _FONTSET[i]

    def stack_pop(self):
        return self._stack.pop()

    def stack_push(self, x: int):
        return self._stack.append(x)


class Display:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("CHIP8")
        self.canvas = pygame.display.set_mode((SCREEN_WIDTH * ZOOM, SCREEN_HEIGHT * ZOOM))
        self.canvas.fill(BG_COLOR)
        pygame.display.update()

    def render(self):
        pass


class Keyboard:
    def poll_event(self):
        pass


class CPU:
    def __init__(self):
        self.memory = Memory()
        # 8 bits register
        self._reg_V = [0] * 16

        # 16 bits register
        self._reg_PC = START_ADDR
        self._reg_I = 0

        self.draw_flag = False
        self._screen_buf = [[0 for _ in range(640)] for _ in range(320)]

        self._keys_pressed_buf = [0] * 16

        self._delay_timer = 0
        self._sound_timer = 0

    def cycle(self):
        pass


class Machine:
    def __init__(self):
        self.display = Display()
        self.keyboard = Keyboard()
        self.cpu = CPU()

    def run(self):
        while True:
            self.cpu.cycle()

            self.keyboard.poll_event()

            self.display.render()


def main():
    machine = Machine()
    machine.run()


if __name__ == '__main__':
    main()
