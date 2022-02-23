import os.path
import random
import pygame
from src.chip8.conf import SCREEN_WIDTH, SCREEN_HEIGHT
from src.chip8.memory import Memory, START_ADDR

from typing import List

_KEY_NUM = 16


class Instruction:

    def __init__(self, val: int):
        self.val = val
        self.opcode = 0
        self.x = 0
        self.y = 0
        self.n = 0
        self.kk = 0
        self.nnn = 0

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

        # Initialize sound
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "beep.mp3"))
        self._IR = None

    def reset_screen(self):
        """ clear screen buffer """
        return [[0 for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    @property
    def screen_buf(self):
        return self._screen_buf

    @property
    def keys_pressed_buf(self):
        return self._keys_pressed_buf

    def load_rom(self, data: List[int]):
        self._memory.write(data)

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
        return self._IR.n

    def cycle(self):
        self.fetch()
        self.decode()
        self.execute()

    def ticker(self):
        if self._delay_timer > 0:
            self._delay_timer -= 1

        if self._sound_timer > 0:
            self._sound_timer -= 1
            pygame.mixer.music.play()

    def fetch(self):
        high_byte = self._memory.ram[self._reg_PC]
        low_byte = self._memory.ram[self._reg_PC + 1]
        instruction = (high_byte << 8) | low_byte
        self._reg_PC += 2
        self._IR = Instruction(instruction)
        return

    def decode(self):
        self._IR.decode()

    def execute(self):

        if self.opcode == 0x0000:
            # 00E0
            # CLS
            # Display
            # clear the display
            if self._IR.kk == 0x00E0:
                self._screen_buf = self.reset_screen()
                self.draw_flag = True
            # 00EE
            # RET
            # Flow
            # return from a subroutine
            elif self._IR.kk == 0x00EE:
                self._reg_PC = self._memory.stack_pop()

        # 1NNN
        # JP addr
        # Flow
        # jump to  nnn
        elif self.opcode == 0x1000:
            addr = self.nnn
            self._reg_PC = addr

        # 2NNN
        # CALL addr
        # Flow
        # call subroutine at nnn
        elif self.opcode == 0x2000:
            addr = self.nnn
            self._memory.stack_push(self._reg_PC)
            self._reg_PC = addr

        # 3XKK
        # SE Vx, byte
        # Cond
        # skip if vx equals kk
        elif self.opcode == 0x3000:
            x = self.x
            kk = self.kk
            if self._reg_V[x] == kk:
                self._reg_PC += 2

        # 4XKK
        # SEN Vx, byte
        # Cond
        # skip if vx not equal to kk
        elif self.opcode == 0x4000:
            x = self.x
            kk = self.kk
            if self._reg_V[x] != kk:
                self._reg_PC += 2

        # 5XY0
        # SE Vx, Vy
        # Cond
        # skip if vx equals vy
        elif self.opcode == 0x5000:
            x = self.x
            y = self.y
            if self._reg_V[x] == self._reg_V[y]:
                self._reg_PC += 2


        # 6XKK
        # LD Vx, byte
        # Const
        # set vx to kk
        elif self.opcode == 0x6000:
            x = self.x
            kk = self.kk
            self._reg_V[x] = kk


        # 7XKK
        # ADD Vx, byte
        # Vx = Vx + kk
        # Const
        # set vx to vx plus kk
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
            # Assig
            # set vx to vy
            if self.flag == 0x0000:
                x = self.x
                y = self.y
                self._reg_V[x] = self._reg_V[y]

            # 8XY1
            # OR Vx, Vy
            # BitOp
            # set vx to vx or vy
            elif self.flag == 0x0001:
                x = self.x
                y = self.y
                self._reg_V[x] |= self._reg_V[y]

            # 8XY2
            # AND Vx, Vy
            # BitOp
            # set vx to vx and vy
            elif self.flag == 0x0002:
                x = self.x
                y = self.y
                self._reg_V[x] &= self._reg_V[y]

            # 8XY3
            # XOR Vx, Vy
            # BitOp
            # set vx to vx xor vy
            elif self.flag == 0x0003:
                x = self.x
                y = self.y
                self._reg_V[x] ^= self._reg_V[y]

            # 8XY4
            # ADD Vx, Vy
            # Math
            # set vx to vx add vy and set vf to carry
            elif self.flag == 0x0004:
                x = self.x
                y = self.y
                self._reg_V[x] += self._reg_V[y]
                self._reg_V[0x0F] = 0x01 if self._reg_V[x] > 0xFF else 0x00
                self._reg_V[x] &= 0xFF

            # 8XY5
            # SUB Vx, Vy
            # Math
            # set vx to vx sub vy
            elif self.flag == 0x0005:
                x = self.x
                y = self.y
                self._reg_V[0x0F] = 0x00 if self._reg_V[x] < self._reg_V[y] else 0x01
                self._reg_V[x] -= self._reg_V[y]
                self._reg_V[x] &= 0xFF

            # 8XY6
            # SHR Vx, {, Vy}
            # BitOp
            # set vx to vy shr 1
            elif self.flag == 0x0006:
                x = self.x
                self._reg_V[0x0F] = self._reg_V[x] & 0x01
                self._reg_V[x] >>= 1

            # 8XY7
            # SUBN Vx, Vy
            # Math
            # set vx to vy - vx , set VF = NOT borrow
            elif self.flag == 0x0007:
                x = self.x
                y = self.y
                self._reg_V[0x0F] = 0x01 if self._reg_V[x] < self._reg_V[y] else 0x00
                self._reg_V[x] = self._reg_V[y] - self._reg_V[x]
                self._reg_V[x] &= 0xFF

            # 8XYE
            # SHL VX, {, Vy}
            # BitOp
            # set vx to vx shl 1
            elif self.flag == 0x000E:
                x = self.x
                self._reg_V[0x0F] = (self._reg_V[x] >> 7) & 0x01
                self._reg_V[x] = self._reg_V[x] << 1
                self._reg_V[x] &= 0xFF


        # 9XY0
        # SNE Vx, Vy
        # Cond
        # skip if vx not equal vy
        elif self.opcode == 0x9000:
            x = self.x
            y = self.y
            if self._reg_V[x] != self._reg_V[y]:
                self._reg_PC += 2

        # ANNN
        # LD I, addr
        # MEM
        # set i to nnn
        elif self.opcode == 0xA000:
            addr = self.nnn
            self._reg_I = addr

        # BNNN
        # JP V0, addr
        # Flow
        # jump to nnn plus v0
        elif self.opcode == 0xB000:
            addr = self.nnn
            self._reg_PC = self._reg_V[0] + addr

        # CXKK
        # RND Vx, byte
        # Rand
        # set vx to random byte and kk
        elif self.opcode == 0xC000:
            x = self.x
            kk = self.kk
            self._reg_V[x] = random.randrange(0, 255) & kk

        # DXYN
        # DRW Vx, Vy, n
        # Display
        # draw to display
        elif self.opcode == 0xD000:
            n = self.n
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
            # KeyOp
            # skip if key equals vx
            if self.kk == 0x009E:
                x = self.x
                if self._keys_pressed_buf[self._reg_V[x]] == 1:
                    self._reg_PC += 2

            # EXA1
            # SKNP Vx
            # KeyOp
            # skip if key not equal to vx
            elif self.kk == 0x00A1:
                x = self.x
                if self._keys_pressed_buf[self._reg_V[x]] == 0:
                    self._reg_PC += 2

        # FX00
        #
        elif self.opcode == 0xF000:
            # FX07
            # LD Vx, DT
            # Timer
            # set vx to delay timer
            if self.kk == 0x0007:
                x = self.x
                self._reg_V[x] = self._delay_timer

            # FX0A
            # LD Vx, K
            # KeyOp
            # store keypress in vx
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
            # Timer
            # set delay timer to vx
            elif self.kk == 0x0015:
                x = self.x
                self._delay_timer = self._reg_V[x]

            # FX18
            # LD ST, Vx
            # Sound
            # set sound timer to vx
            elif self.kk == 0x0018:
                x = self.x
                self._sound_timer = self._reg_V[x]

            # FX1E
            # ADD I, Vx
            # MEM
            # set i to i plus vx
            elif self.kk == 0x001E:
                x = self.x
                self._reg_I += self._reg_V[x]

            # FX29
            # LD F, Vx
            # MEM
            # set i to sprite location for vx
            elif self.kk == 0x0029:
                x = self.x
                self._reg_I = self._reg_V[x] * 5
            # FX33
            # LD B, Vx
            # BCD
            # store bcd in i
            elif self.kk == 0x0033:
                x = self.x
                self._memory.ram[self._reg_I] = self._reg_V[x] // 100
                self._memory.ram[self._reg_I + 1] = (self._reg_V[x] % 100) // 10
                self._memory.ram[self._reg_I + 2] = (self._reg_V[x] % 100) % 10
            # FX55
            # LD [I], Vx
            # MEM
            # store v0 to vx in memory from location i
            elif self.kk == 0x0055:
                x = self.x
                for i in range(x + 1):
                    self._memory.ram[self._reg_I + i] = self._reg_V[i]
            # FX65
            # LD Vx, [I]
            # MEM
            # fill v0 to vx from memory location i
            elif self.kk == 0x0065:
                x = self.x
                for i in range(x + 1):
                    self._reg_V[i] = self._memory.ram[self._reg_I + i]
