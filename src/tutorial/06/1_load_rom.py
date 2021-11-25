import sys
from typing import List, Optional
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

_KEYS = {
    pygame.K_1: 0x1, pygame.K_2: 0x2, pygame.K_3: 0x3, pygame.K_4: 0xC,
    pygame.K_q: 0x4, pygame.K_w: 0x5, pygame.K_e: 0x6, pygame.K_r: 0xD,
    pygame.K_a: 0x7, pygame.K_s: 0x8, pygame.K_d: 0x9, pygame.K_f: 0xE,
    pygame.K_z: 0xA, pygame.K_x: 0x0, pygame.K_c: 0xB, pygame.K_v: 0xF
}


def load_file(filepath: str) -> Optional[List[int]]:
    try:
        data = []
        with open(filepath, "rb") as f:
            file_bytes = f.read()
            for i in range(len(file_bytes)):
                data.append(int(file_bytes[i]))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
    return data


class Memory:

    def __init__(self):
        # 4KB memory
        self._ram = [0] * 4 * 1024
        # stack
        self._stack = []
        for i in range(len(_FONTSET)):
            self._ram[i] = _FONTSET[i]

    @property
    def ram(self):
        return self._ram

    def write(self, data: List[int]):
        for i in range(len(data)):
            self._ram[START_ADDR + i] = int(data[i])

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


class Keyboard:
    def poll_event(self):
        pass


class Instruction:

    def __init__(self, val: int):
        self.val = val
        self.opcode = 0
        self.x = 0
        self.y = 0
        self.n = 0
        self.kk = 0
        self.nnn = 0
        self.flag = 0

    def decode_opcode(self) -> int:
        return self.val & 0xF000

    def decode_x(self) -> int:
        return (self.val & 0x0F00) >> 8

    def decode_y(self) -> int:
        return (self.val & 0x00F0) >> 4

    def decode_n(self) -> int:
        return self.val & 0x000F

    def decode_kk(self) -> int:
        return self.val & 0x00FF

    def decode_nnn(self) -> int:
        return self.val & 0x0FFF

    def decode(self):
        self.opcode = self.decode_opcode()
        self.x = self.decode_x()
        self.y = self.decode_y()
        self.n = self.decode_n()
        self.kk = self.decode_kk()
        self.nnn = self.decode_nnn()
        self.flag = self.decode_n()


class CPU:
    def __init__(self):
        self._memory = Memory()
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

        self._IR = None

    @property
    def memory(self):
        return self._memory

    def load_rom(self, data: List[int]):
        self._memory.write(data)

    def fetch(self):
        high_byte = self._memory.ram[self._reg_PC]
        low_byte = self._memory.ram[self._reg_PC + 1]
        instruction = (high_byte << 8) | low_byte
        self._reg_PC += 2
        self._IR = Instruction(instruction)

    def decode(self):
        self._IR.decode()

    def execute(self):
        pass

    def cycle(self):
        self.fetch()
        self.decode()
        self.execute()


class Machine:
    def __init__(self):
        self.display = Display()
        self.keyboard = Keyboard()
        self.cpu = CPU()

    def load_rom(self, rom_file: str):
        data = load_file(rom_file)
        self.cpu.load_rom(data)

    def run(self):
        while True:
            self.cpu.cycle()

            self.keyboard.poll_event()

            self.display.render(self.cpu._screen_buf)


def main():
    machine = Machine()
    machine.run()


if __name__ == '__main__':
    main()
