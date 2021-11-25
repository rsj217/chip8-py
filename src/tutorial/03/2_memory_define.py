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

    def render(self):
        pass


class Keyboard:
    def poll_event(self):
        pass


class CPU:
    def __init__(self):
        self.memory = Memory()

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
