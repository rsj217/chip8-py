from src.chip8.machine import Machine


def main(rom_file):
    try:
        machine = Machine()
        machine.load_rom(rom_file)
        machine.run()
    except Exception as e:
        print(f"Err: {e}")
        print("python3 -m src.main --path=./roms/BC")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='rom path', required=True)
    args = parser.parse_args()

    main(args.path)








