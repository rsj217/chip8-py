基本指令
==============

[屏幕绘制](./04_display_draw.md) 一节，我们通过指定屏幕二维数组 screen_buf 在屏幕显示了 `IBM`
的图案。本节的目标就是使用 Chip8 加载 ibm 的 rom 文件，通过 CPU 的解析执行 Chip8 指令，来显示 IBM 的图像。

## 二进制

chip8 的 rom 文件都是二进制文件。使用 python 可以很方便的读取。下面是代码:

```{eval-rst}
.. autofunction:: src.tutorial.06.1_load_rom.load_file
```

```python 
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
```

Machine 类也增加`load_rom`方法

```{eval-rst}
.. automethod:: src.tutorial.06.1_load_rom.Machine.load_rom
```

```python 
class Machine:

    def load_rom(self, rom_file: str):
        data = load_file(rom_file)
        self.cpu.load_rom(data)
```

Memory 类增加读取 rom 到ram中

```{eval-rst}
.. autofunction:: src.tutorial.06.1_load_rom.Memory.write
```

```python 
    def write(self, data: List[int]):
        for i in range(len(data)):
            self._ram[START_ADDR + i] = int(data[i])
```

chip8用户程序的内存地址是`0x200`开始的，因此读取rom的数据也从`0x200`开始。

## IBM

使用十六进制编辑器可以打开`IBM.bin`的rom文件，然后看到其数据为 ：

```text 
0x00, 0xe0, 0xa2, 0x2a, 0x60, 0x0c, 0x61, 0x08, 0xd0, 0x1f, 0x70, 0x09, 0xa2, 0x39, 0xd0, 0x1f,
0xa2, 0x48, 0x70, 0x08, 0xd0, 0x1f, 0x70, 0x04, 0xa2, 0x57, 0xd0, 0x1f, 0x70, 0x08, 0xa2, 0x66,
0xd0, 0x1f, 0x70, 0x08, 0xa2, 0x75, 0xd0, 0x1f, 0x12, 0x28, 0xff, 0x00, 0xff, 0x00, 0x3c, 0x00,
0x3c, 0x00, 0x3c, 0x00, 0x3c, 0x00, 0xff, 0x00, 0xff, 0xff, 0x00, 0xff, 0x00, 0x38, 0x00, 0x3f,
0x00, 0x3f, 0x00, 0x38, 0x00, 0xff, 0x00, 0xff, 0x80, 0x00, 0xe0, 0x00, 0xe0, 0x00, 0x80, 0x00,
0x80, 0x00, 0xe0, 0x00, 0xe0, 0x00, 0x80, 0xf8, 0x00, 0xfc, 0x00, 0x3e, 0x00, 0x3f, 0x00, 0x3b,
0x00, 0x39, 0x00, 0xf8, 0x00, 0xf8, 0x03, 0x00, 0x07, 0x00, 0x0f, 0x00, 0xbf, 0x00, 0xfb, 0x00,
0xf3, 0x00, 0xe3, 0x00, 0x43, 0xe0, 0x00, 0xe0, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80, 0x00, 0x80,
0x00, 0xe0, 0x00, 0xe0
```

反汇编为如下的指令：

```text
start:
             0x0200     CLS
             0x0202     LD I, lbl_0x022a
             0x0204     LD V0, 0x0c
             0x0206     LD V1, 0x08
             0x0208     DRW V0, V1, 0x0f
             0x020a     ADD V0, 0x09
             0x020c     LD I, lbl_0x0239
             0x020e     DRW V0, V1, 0x0f
             0x0210     LD I, lbl_0x0248
             0x0212     ADD V0, 0x08
             0x0214     DRW V0, V1, 0x0f
             0x0216     ADD V0, 0x04
             0x0218     LD I, lbl_0x0257
             0x021a     DRW V0, V1, 0x0f
             0x021c     ADD V0, 0x08
             0x021e     LD I, lbl_0x0266
             0x0220     DRW V0, V1, 0x0f
             0x0222     ADD V0, 0x08
             0x0224     LD I, lbl_0x0275
             0x0226     DRW V0, V1, 0x0f
lbl_0x0228:
             0x0228     JP lbl_0x0228
lbl_0x022a:
             0x022a     DB 0xff    ; 11111111
             0x022b     DB 0x00    ;
             0x022c     DB 0xff    ; 11111111
             0x022d     DB 0x00    ;
             0x022e     DB 0x3c    ;   1111
             0x022f     DB 0x00    ;
             0x0230     DB 0x3c    ;   1111
             0x0231     DB 0x00    ;
             0x0232     DB 0x3c    ;   1111
             0x0233     DB 0x00    ;
             0x0234     DB 0x3c    ;   1111
             0x0235     DB 0x00    ;
             0x0236     DB 0xff    ; 11111111
             0x0237     DB 0x00    ;
             0x0238     DB 0xff    ; 11111111
lbl_0x0239:
             0x0239     DB 0xff    ; 11111111
             0x023a     DB 0x00    ;
             0x023b     DB 0xff    ; 11111111
             0x023c     DB 0x00    ;
             0x023d     DB 0x38    ;   111
             0x023e     DB 0x00    ;
             0x023f     DB 0x3f    ;   111111
             0x0240     DB 0x00    ;
             0x0241     DB 0x3f    ;   111111
             0x0242     DB 0x00    ;
             0x0243     DB 0x38    ;   111
             0x0244     DB 0x00    ;
             0x0245     DB 0xff    ; 11111111
             0x0246     DB 0x00    ;
             0x0247     DB 0xff    ; 11111111
lbl_0x0248:
             0x0248     DB 0x80    ; 1
             0x0249     DB 0x00    ;
             0x024a     DB 0xe0    ; 111
             0x024b     DB 0x00    ;
             0x024c     DB 0xe0    ; 111
             0x024d     DB 0x00    ;
             0x024e     DB 0x80    ; 1
             0x024f     DB 0x00    ;
             0x0250     DB 0x80    ; 1
             0x0251     DB 0x00    ;
             0x0252     DB 0xe0    ; 111
             0x0253     DB 0x00    ;
             0x0254     DB 0xe0    ; 111
             0x0255     DB 0x00    ;
             0x0256     DB 0x80    ; 1
lbl_0x0257:
             0x0257     DB 0xf8    ; 11111
             0x0258     DB 0x00    ;
             0x0259     DB 0xfc    ; 111111
             0x025a     DB 0x00    ;
             0x025b     DB 0x3e    ;   11111
             0x025c     DB 0x00    ;
             0x025d     DB 0x3f    ;   111111
             0x025e     DB 0x00    ;
             0x025f     DB 0x3b    ;   111 11
             0x0260     DB 0x00    ;
             0x0261     DB 0x39    ;   111  1
             0x0262     DB 0x00    ;
             0x0263     DB 0xf8    ; 11111
             0x0264     DB 0x00    ;
             0x0265     DB 0xf8    ; 11111
lbl_0x0266:
             0x0266     DB 0x03    ;       11
             0x0267     DB 0x00    ;
             0x0268     DB 0x07    ;      111
             0x0269     DB 0x00    ;
             0x026a     DB 0x0f    ;     1111
             0x026b     DB 0x00    ;
             0x026c     DB 0xbf    ; 1 111111
             0x026d     DB 0x00    ;
             0x026e     DB 0xfb    ; 11111 11
             0x026f     DB 0x00    ;
             0x0270     DB 0xf3    ; 1111  11
             0x0271     DB 0x00    ;
             0x0272     DB 0xe3    ; 111   11
             0x0273     DB 0x00    ;
             0x0274     DB 0x43    ;  1    11
lbl_0x0275:
             0x0275     DB 0xe0    ; 111
             0x0276     DB 0x00    ;
             0x0277     DB 0xe0    ; 111
             0x0278     DB 0x00    ;
             0x0279     DB 0x80    ; 1
             0x027a     DB 0x00    ;
             0x027b     DB 0x80    ; 1
             0x027c     DB 0x00    ;
             0x027d     DB 0x80    ; 1
             0x027e     DB 0x00    ;
             0x027f     DB 0x80    ; 1
             0x0280     DB 0x00    ;
             0x0281     DB 0xe0    ; 111
             0x0282     DB 0x00    ;
             0x0283     DB 0xe0    ; 111

```

地址 `0x0200 ~ 0x0228` 是 rom 的指令，`0x22a ~ 0x283` 是数据。 从数据可以看到，chip8 以 sprite 方式绘图。[^1] 如`0x22a ~ 0x238` 是`15-byte`的sprite。 Sprite绘图方式将在后面介绍。

由此可见，想要打印 IBM 的突然，只需要实现下面几个指令：

* 00E0: 清屏 CLS
* 1NNN: 跳转 JP NNN
* 6XKK: 设置寄存器 LD Vx, KK
* 7XKK: 将值添加到寄存器 ADD Vx, KK
* ANNN: 设置地址寄存器 LD I, NNN
* DXYN: 显示/绘制 DRW Vx, Vy, N


这些指令放在 CPU.execute 方法实现。这是一个巨大的`if elif` 语句。[^2]

### 指令执行

CPU.execute 方法实现指令的执行。下面是这几条指令的代码。

```{eval-rst}
.. automethod:: src.tutorial.06.2_ibm_rom.CPU.execute
```

```python 
    def execute(self):

        if self.opcode == 0x0000:
            # 00E0
            # CLS
            # clear the display
            if self._IR.kk == 0x00E0:
                self._screen_buf = self.reset_screen()
                self.draw_flag = True

        # 1NNN
        # JP addr
        # jump to location nnn
        elif self.opcode == 0x1000:
            addr = self.nnn
            self._reg_PC = addr


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

        # ANNN
        # LD I, addr
        # I = nnn
        elif self.opcode == 0xA000:
            addr = self.nnn
            self._reg_I = addr

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
```

下面针对这些代码进行解析。

**00E0**，清屏的指令，只需要将视频缓存二维数组 screen_buf 恢复成默认，即所有元素都是 0 值。

**1NNN** 跳转指令，decode 指令得到 NNN，这是跳转的地址。然后将 PC 寄存器的值指向这个地址。即程序的执行流将会从跳转地址开始 fetch 下一条指令。类似高级语言的`goto`语句。

**6XKK** 设置寄存器 Vx 的值为 KK。decode可以得到 x 和 KK 的值，直接设置 reg_V 对应的值即可。类似高级语言的赋值语句 Vx = KK

**7XKK** 将寄存器Vx的值加上 KK，然后再存储回 Vx。类似高级语言的 += 语句。Vx = Vx + KK。通用寄存器的大小是 1-byte，加法操作会溢出。溢出之后需要抹去高位，Vx 会和 0xFF 做`与`(&)操作。但是这条指令不需要设置标记位(reg_V[0xF])。

**ANNN** 设置地址寄存器I的值为 NNN。这条指令与`1NNN` 类似。都是设置寄存器的值为一个地址。不同在于这条指令修改的是索引寄存器。

**DXYN** 这一条绘图指令。Chip8 绘图使用 Sprite 方式。Sprite 即一个区域块。如下图所示，IBM logo的图案，由6个 sprite 组成。每一个 spite 是 8 * 15 的像素块，由不同的颜色标识。其中字母`I`正好是一个 sprite。字母`B`由 蓝色和绿色的两个 sprite 组成。其中绿色的 spite 和组成`M`的黄色的 sprite 有重叠。因为重叠的地方绿色 sprite 没有像素，这样的覆盖也不会影响最终的视觉效果。

```{image} ../img/sprite.png
:alt: sprite
:align: center
```

sprite 的大小固定(15*8)，因此绘制 sprite 的时候，只需要指定起点的坐标即可。例如`I`的起点坐标是(12, 8)，即存储在 Vx 和 Vy 的值。以此类推，字母 B 的蓝色 sprite 的起点是(12+9, 8)。

尽管 sprite 的大小是固定的，但是 sprite 上的图案可以自由绘制，不同的 sprite 块可以叠加以绘制最终效果。就像字母`B`和字母`M`重叠的部分。

对于指令 DXYN 而言，(x, y) 的值分别为 Vx 和 Vy 的值。N 表示从地址寄存器 reg_I 读取 N-byte 的数据。这些数据用二进制进行表示。0 表示不需要绘图，1 表示需要绘制。通过解析数据的二进制位，写到视频缓存二维数组 screen_buf 中。再交给 display 去绘图。

执行改指令的代码会先 decode Vx 和 Vy，然后取 [reg_I， reg_I + N) 这一段空间的数据。 再针对这些数据进行遍历，求出当前 sprite 的起点坐标(x_cord, y_cord)。

如果当前点的值(sys_bit)与需要绘制的bit的`与`操作为1，则需要设置标记寄存器 reg_V[0xF]的值为1。最后该值与sys_bit做异或（^）操作。

指令完成之前，设置一个 CPU 的 draw_flag 属性，表示此时主循环需要绘制一帧图形。

实现上面的指令之后，还需要处理一下`键盘事件`，给键盘事件增加退出监听，不然我们的模拟器会被卡住。

```{eval-rst}
.. automethod:: src.tutorial.06.3_run_rom.Keyboard.poll_event
```

```python 
    def poll_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
```

```{eval-rst}
.. autofunction:: src.tutorial.06.3_run_rom.main
```

之后，屏幕就会输出 IBM 的图案。

```{image} ../img/ibm-logo.png
:alt: ibm-logo
:align: center
```

## 总结

本节的主要内容是了解 Chip8 CPU 循环的主要工作流。同时实现 SPEC 上描述的几条基本指令。比较重要的是绘图指令`DXYN`。掌握Chip8图像绘制的`Sprite`方法。

接下来的任务就很简单了，就是根据 SPEC，将剩余的指令实现完成，模拟器就基本完成了。

[^1]: Sprite 绘图方式一直很流行
[^2]: Python3.10提供了`match`语句，对于这种应用场景实现会更优雅。rust 的`match pattern`也十分合适。
