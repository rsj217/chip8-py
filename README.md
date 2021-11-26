# chip8-py


Chip8 Emulator in Python3

### install

```shell
$ git clone git@github.com:rsj217/chip8-py.git
$ cd chip8-py
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

### run rom

```shell
(venv)  python3 -m src.main --help

Hello from the pygame community. https://www.pygame.org/contribute.html
usage: main.py [-h] --path PATH

optional arguments:
  -h, --help   show this help message and exit
  --path PATH  rom path
  
(venv)  python3 -m src.main --path=your rom path

```

### build document

There is an online [document](https://rsj217.github.io/chip8-py/) that generate by sphinx doc and publish by github pages. 
You can also fetch the source doc and build by yourself.

```shell
$ cd docs && rm build
$ make html 
$ open index.html
```

[Golang Version](https://github.com/rsj217/chip8-go)