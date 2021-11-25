import sys
from typing import List, Optional
import random
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

_KEY_NUM = 16

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


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
        # 8 bits register
        self._reg_V = [0] * 16

        # 16 bits register
        self._reg_PC = START_ADDR
        self._reg_I = 0

        self._memory = Memory()
        self.draw_flag = False
        self._screen_buf = self.reset_screen()

        self._keys_pressed_buf = [0] * _KEY_NUM

        self._delay_timer = 0
        self._sound_timer = 0

        self._IR = None

    def reset_screen(self):
        """ clear screen buffer """
        return [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    @property
    def screen_buf(self):
        return self._screen_buf

    @property
    def opcode(self) -> int:
        return self._IR.opcode

    @property
    def x(self) -> int:
        return self._IR.x

    @property
    def y(self) -> int:
        return self._IR.y

    @property
    def n(self) -> int:
        return self._IR.n

    @property
    def kk(self) -> int:
        return self._IR.kk

    @property
    def nnn(self) -> int:
        return self._IR.nnn

    @property
    def flag(self) -> int:
        return self._IR.flag

    def load_rom(self, data: List[int]):
        self._memory.write(data)

    def cycle(self):
        self.fetch()
        self.decode()
        self.execute()

    def fetch(self):
        high_byte = self._memory.ram[self._reg_PC]
        low_byte = self._memory.ram[self._reg_PC + 1]
        instruction = (high_byte << 8) | low_byte
        self._reg_PC += 2
        self._IR = Instruction(instruction)

    def decode(self):
        self._IR.decode()

    def execute(self):

        if self.opcode == 0x0000:
            # 00E0
            # CLS
            # clear the display
            if self._IR.kk == 0x00E0:
                self._screen_buf = self.reset_screen()
                self.draw_flag = True
            # 00EE
            # RET
            # return from a subroutine
            elif self._IR.kk == 0x00EE:
                self._reg_PC = self._memory.stack_pop()

        # 1NNN
        # JP addr
        # jump to location nnn
        elif self.opcode == 0x1000:
            addr = self.nnn
            self._reg_PC = addr

        # 2NNN
        # CALL addr
        # call subroutine at nnn
        elif self.opcode == 0x2000:
            addr = self.nnn
            self._memory.stack_push(self._reg_PC)
            self._reg_PC = addr

        # 3XKK
        # SE Vx, byte
        #
        elif self.opcode == 0x3000:
            x = self.x
            kk = self.kk
            if self._reg_V[x] == kk:
                self._reg_PC += 2

        # 4XKK
        # SEN Vx, byte
        elif self.opcode == 0x4000:
            x = self.x
            kk = self.kk
            if self._reg_V[x] != kk:
                self._reg_PC += 2

        # 5XY0
        # SE Vx, Vy
        elif self.opcode == 0x5000:
            x = self.x
            y = self.y
            if self._reg_V[x] == self._reg_V[y]:
                self._reg_PC += 2

        # 6XKK
        # LD Vx, byte
        # Vx = kk
        elif self.opcode == 0x6000:
            x = self.x
            kk = self.kk
            self._reg_V[x] = kk


        # 7XKK
        # ADD Vx, byte
        # Vx = Vx + kk
        elif self.opcode == 0x7000:
            x = self.x
            kk = self.kk
            self._reg_V[x] += kk
            self._reg_V[x] &= 0xff

        # 8XYN
        # Logical and arithmetic instructions
        elif self.opcode == 0x8000:
            # 8XY0
            # LD Vx, Vy
            # set vx to vy
            if self.flag == 0x0000:
                x = self.x
                y = self.y
                self._reg_V[x] = self._reg_V[y]

            # 8XY1
            # OR Vx, Vy
            # set vx to vx or vy
            elif self.flag == 0x0001:
                x = self.x
                y = self.y
                self._reg_V[x] |= self._reg_V[y]

            # 8XY2
            # AND Vx, Vy
            # set vx to vx and vy
            elif self.flag == 0x0002:
                x = self.x
                y = self.y
                self._reg_V[x] &= self._reg_V[y]

            # 8XY3
            # XOR Vx, Vy
            # set vx to vx xor vy
            elif self.flag == 0x0003:
                x = self.x
                y = self.y
                self._reg_V[x] ^= self._reg_V[y]

            # 8XY4
            # ADD Vx, Vy
            # set vx to vx add vy  and set vf to carry
            elif self.flag == 0x0004:
                x = self.x
                y = self.y
                self._reg_V[x] += self._reg_V[y]
                self._reg_V[0x0F] = 0x01 if self._reg_V[x] > 0xFF else 0x00
                self._reg_V[x] &= 0xFF

            # 8XY5
            # SUB Vx, Vy
            # set vx to vx sub vy
            elif self.flag == 0x0005:
                x = self.x
                y = self.y
                self._reg_V[0x0F] = 0x00 if self._reg_V[x] < self._reg_V[y] else 0x01
                self._reg_V[x] -= self._reg_V[y]
                self._reg_V[x] &= 0xFF

            # 8XY6
            # SHR Vx, {, Vy}
            # set vx = vy SHR 1
            elif self.flag == 0x0006:
                x = self.x
                self._reg_V[0x0F] = self._reg_V[x] & 0x01
                self._reg_V[x] >>= 1

            # 8XY7
            # SUBN Vx, Vy
            # set vx = vy - vx set VF = NOT borrow
            elif self.flag == 0x0007:
                x = self.x
                y = self.y
                self._reg_V[0x0F] = 0x01 if self._reg_V[x] < self._reg_V[y] else 0x00
                self._reg_V[x] = self._reg_V[y] - self._reg_V[x]
                self._reg_V[x] &= 0xFF

            # 8XYE
            # SHL VX, {, Vy}
            #
            elif self.flag == 0x000E:
                x = self.x
                self._reg_V[0x0F] = (self._reg_V[x] >> 7) & 0x01
                self._reg_V[x] = self._reg_V[x] << 1
                self._reg_V[x] &= 0xFF

        # 9XY0
        elif self.opcode == 0x9000:
            x = self.x
            y = self.y
            if self._reg_V[x] != self._reg_V[y]:
                self._reg_PC += 2

        # ANNN
        # LD I, addr
        # I = nnn
        elif self.opcode == 0xA000:
            addr = self.nnn
            self._reg_I = addr

        # BNNN
        # JP V0, addr
        elif self.opcode == 0xB000:
            addr = self.nnn
            self._reg_PC = self._reg_V[0] + addr

        # CXKK
        # RND Vx, byte
        #
        elif self.opcode == 0xC000:
            x = self.x
            kk = self.kk
            self._reg_V[x] = random.randrange(0, 255) & kk


        # DXYN
        # DRW Vx, Vy, n
        elif self.opcode == 0xD000:
            n = self.flag
            x = self.x
            y = self.y

            vx = self._reg_V[x]
            vy = self._reg_V[y]

            self._reg_V[0xF] = 0
            for yy in range(n):
                sys_byte = self._memory.ram[self._reg_I + yy]
                for xx in range(8):
                    x_cord = vx + xx
                    y_cord = vy + yy
                    if x_cord < SCREEN_WIDTH and y_cord < SCREEN_HEIGHT:
                        sys_bit = (sys_byte >> (7 - xx)) & 0x01
                        if (self._screen_buf[y_cord][x_cord] & sys_bit) == 1:
                            self._reg_V[0xF] = 1

                        self._screen_buf[y_cord][x_cord] ^= sys_bit

            self.draw_flag = True

        elif self.opcode == 0xE000:
            # EX9E
            # SKP Vx
            if self.kk == 0x009E:
                x = self.x
                if self._keys_pressed_buf[self._reg_V[x]] == 1:
                    self._reg_PC += 2

            # EXA1
            # SKNP Vx
            elif self.kk == 0x00A1:
                x = self.x
                if self._keys_pressed_buf[self._reg_V[x]] == 0:
                    self._reg_PC += 2
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX07
            # LD Vx, DT
            if self.kk == 0x0007:
                x = self.x
                self._reg_V[x] = self._delay_timer

            # FX0A
            # LD Vx, K
            elif self.kk == 0x000A:
                x = self.x
                pressed = False
                for i in range(16):
                    if self._keys_pressed_buf[i] == 1:
                        self._reg_V[x] = i
                        pressed = True
                        break
                if not pressed:
                    self._reg_PC -= 2

            # FX15
            # LD DT, Vx
            elif self.kk == 0x0015:
                x = self.x
                self._delay_timer = self._reg_V[x]

            # FX18
            # LD ST, Vx
            elif self.kk == 0x0018:
                x = self.x
                self._sound_timer = self._reg_V[x]

            # FX1E
            # ADD I, Vx
            elif self.kk == 0x001E:
                x = self.x
                self._reg_I += self._reg_V[x]



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
            if self.cpu.draw_flag:
                self.display.render(self.cpu.screen_buf)
                self.cpu.draw_flag = False


def main():
    rom_file = "../../../roms/OPCODE"
    machine = Machine()
    machine.load_rom(rom_file)
    machine.run()


if __name__ == '__main__':
    main()
