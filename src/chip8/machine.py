import sys
import time
from typing import List
from src.chip8.display import Display
from src.chip8.keyboard import Keyboard
from src.chip8.cpu import CPU
from src.chip8.conf import CLOCK_SPEED, TIMER_SPEED


def load_file(filepath: str) -> List[int]:
    data = []
    with open(filepath, "rb") as f:
        file_bytes = f.read()
        for i in range(len(file_bytes)):
            data.append(int(file_bytes[i]))
    return data


class Machine:
    def __init__(self):
        self.display = Display()
        self.keyboard = Keyboard()
        self.cpu = CPU()

    def load_rom(self, rom_file: str):
        data = load_file(rom_file)
        self.cpu.load_rom(data)

    def run(self):
        cycles = 0
        while True:

            self.cpu.cycle()

            self.keyboard.poll_event(self.cpu.keys_pressed_buf)

            if self.cpu.draw_flag:
                self.display.render(self.cpu.screen_buf)
                self.cpu.draw_flag = False

            cycles += 1
            time.sleep(1 / CLOCK_SPEED)
            if cycles >= CLOCK_SPEED / TIMER_SPEED:
                cycles = 0
                self.cpu.ticker()

    def exit(self):
        self.display.quit()
        sys.exit()
