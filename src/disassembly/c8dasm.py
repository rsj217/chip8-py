import sys
from typing import List, Optional
from collections import deque


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


START_ADDR = 0x200


class Disassembler:
    def __init__(self):
        self.ram = [0] * 4 * 1024
        self._reg_PC = START_ADDR
        self._label = set()
        self._codemap = set()

        self.max_addr = 0
        self.rom_size = 0

    def load_rom(self, filename: str):
        data = load_file(filename)
        self.rom_size = len(data)
        self.max_addr = START_ADDR + self.rom_size

        for i in range(len(data)):
            self.ram[START_ADDR + i] = int(data[i])

        print(";----------------------------------------------------")
        print(f"; ROM Name: {filename}")
        print(f"; ROM Size: {self.rom_size}  Bytes")
        print(";----------------------------------------------------")

    def discover(self):

        segments = deque()
        segments.append(START_ADDR)

        while len(segments) != 0:
            self.pc = segments.popleft()

            while self.pc < self.max_addr and self.pc not in self._codemap:
                opcode = (self.ram[self.pc] << 8) | self.ram[self.pc + 1]

                self._codemap.add(self.pc)

                self.pc += 2

                if opcode == 0x00EE:
                    break

                if opcode & 0xF000 == 0x1000:
                    self.pc = opcode & 0x0FFF
                    self._label.add(self.pc)
                elif opcode & 0xF000 == 0x2000:
                    segments.append(self.pc)
                    self.pc = opcode & 0x0FFF
                    self._label.add(self.pc)
                elif opcode & 0xF000 in (0x3000, 0x4000, 0x5000, 0x9000):
                    segments.append(self.pc + 2)
                elif opcode & 0xF000 == 0xE000:
                    if opcode & 0xF0FF in (0xE09E, 0xE0A1):
                        segments.append(self.pc + 2)
                elif opcode & 0xF000 == 0xA000:
                    self._label.add(opcode & 0x0FFF)
                elif opcode & 0xF000 == 0xB000:
                    raise

    def render(self):
        count = 0
        self.pc = START_ADDR

        while self.pc < self.max_addr:
            if self.pc in self._label:
                if count > 0:
                    print()
                    count = 0

                print('L{:03X}:'.format(self.pc))

            if self.pc not in self._codemap:
                if count == 0:
                    print("\tDB #{:02X}".format(self.ram[self.pc] & 0xFF), end="")
                else:
                    print(", #{:02X}".format(self.ram[self.pc] & 0xFF), end="")

                count += 1
                if count % 4 == 0:
                    print()
                    count = 0

                self.pc += 1
                continue

            if count > 0:
                print(count)
                count = 0

            opcode = (self.ram[self.pc] << 8) | self.ram[self.pc + 1]
            print("\t{:<30}; 0x{:04X}".format(format(opcode), opcode))
            self.pc += 2


def format(opcode):
    addr = (opcode & 0x0fff)
    x = (opcode & 0x0f00) >> 8
    y = (opcode & 0x00f0) >> 4
    value = (opcode & 0x00ff)
    group = (opcode & 0xF000)

    # retrieve the instruction from the opcode value
    if group == 0x0000:
        if (opcode == 0x00E0):
            return "CLS"

        if (opcode == 0x00EE):
            return "RET"

    if group == 0x1000:  # JP addr
        return "JP   L{:03X}".format(addr)

    if group == 0x2000:  # CALL addr
        return "CALL L{:03X}".format(addr)

    if group == 0x3000:  # SE Vx, value
        return "SE   V{}, #{:02X}".format(x, value)

    if group == 0x4000:  # SNE Vx, value
        return "SNE  V{}, #{:02X}".format(x, value)

    if group == 0x5000:  # SE Vx, Vy
        return "SE   V{}, V{}".format(x, y)

    if group == 0x6000:  # LD Vx, value
        return "LD   V{}, #{:02X}".format(x, value)

    if group == 0x7000:  # ADD Vx, value
        return "ADD  V{}, #{:02X}".format(x, value)

    if group == 0x8000:
        if opcode & 0x000F:
            if opcode & 0x000F == 0x0000:  # LD Vx, Vy
                return "LD   V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0001:  # OR Vx, Vy
                return "OR   V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0002:  # AND Vx, Vy
                return "AND  V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0003:  # XOR Vx, Vy
                return "XOR  V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0004:  # ADC Vx, Vy
                return "ADD  V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0005:  # SBC Vx, Vy
                return "SUB  V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x0006:  # SHR Vx, 1
                return "SHR  V{}, #1".format(x)
            if opcode & 0x000F == 0x0007:  # SUBN Vx, Vy
                return "SUBN V{}, V{}".format(x, y)
            if opcode & 0x000F == 0x000E:  # SHL Vx, 1
                return "SHL  V{}, #1".format(x)

    if group == 0x9000:  # SNE Vx, Vy
        return "SNE  V{}, V{}".format(x, y)

    if group == 0xA000:  # LD I, addr
        return "LD   I, L{:03X}".format(addr)

    if group == 0xB000:  # JP V0, addr
        return "JP   V0, L{:03X}".format(addr)

    if group == 0xC000:  # RND Vx, value
        return "RND  V{}, 0x{:02X}".format(x, value)

    if group == 0xD000:  # DRW Vx, Vy, n
        return "DRW  V{}, V{}, #{:02X}".format(x, y, value & 0x000F)

    if group == 0xE000:
        # SKP Vx
        if ((opcode & 0x00FF) == 0x009E):
            return "SKP  V{}".format(x)

        # SKNP Vx
        if ((opcode & 0x00FF) == 0x00A1):
            return "SKNP V{}".format(x)

    if group == 0xF000:
        if opcode & 0x00FF == 0x0007:  # LD Vx, DT
            return "LD   V{}, DT".format(x)
        if opcode & 0x00FF == 0x000A:  # LD Vx, K
            return "LD   V{}, K".format(x)
        if opcode & 0x00FF == 0x0015:  # LD DT, Vx
            return "LD   DT, V{}".format(x)
        if opcode & 0x00FF == 0x0018:  # LD ST, Vx
            return "LD   ST, V{}".format(x)
        if opcode & 0x00FF == 0x001E:  # ADD I, Vx
            return "ADD  I, V{}".format(x)
        if opcode & 0x00FF == 0x0029:  # LD F, Vx
            return "LD   F, V{}".format(x)
        if opcode & 0x00FF == 0x0033:  # LD B, Vx
            return "LD   B, V{}".format(x)
        if opcode & 0x00FF == 0x0055:  # LD [I], Vx
            return "LD   [I], V{}".format(x)
        if opcode & 0x00FF == 0x0065:  # LD Vx, [I]
            return "LD   V{}, [I]".format(x)

    return "(0x{:04X})".format(opcode)


def main():
    disassembler = Disassembler()
    disassembler.load_rom("../../roms/TETRIS")
    disassembler.discover()
    disassembler.render()


if __name__ == '__main__':
    main()
