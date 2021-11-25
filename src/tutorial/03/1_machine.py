class Memory:
    pass


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
