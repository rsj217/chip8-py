更多指令
==============

## 指令测试

实现[基本指令](06_base_instruction.md) 介绍的指令，可以在屏幕输出 IBM 的 logo。软件开发中，测试一直很重要。目前我们还没有编写任何测试代码。仅仅使用视觉测试，即通过运行程序查看结果。在开发初期，这也未尝不可。

针对 Chip8 的指令有两个著名的测试 rom。[^1] [BC](https://github.com/daniel5151/AC8E/blob/master/roms/bc_test.ch8)和[OPCODE](https://github.com/corax89/chip8-test-rom) 运行这两个 rom，如果指令正确。就会得出如下的图：

* BC Test

```{image} ../img/bc.png
:alt: bc
:align: center
```

屏幕会打印 `Bon By BestCode.` 的图案。如果某些指令出错。则会显示对应的错误码。具体的错误说明可以查看[bc_test.txt](https://github.com/daniel5151/AC8E/blob/master/roms/bc_test.txt) 

* OPCODE Test

```{image} ../img/opcode.png
:alt: opcode
:align: center
```

屏幕会显示这些指令的测试是否通过，OK表示通过，NO表示未通过。屏幕的指令说明如下：

```text
3XNN	00EE	8XY5
4XNN	8XY0	8XY6
5XY0	8XY1	8XYE
7XNN	8XY2	FX55
9XY0	8XY3	FX33
ANNN	8XY4	1NNN
```

使用这两个 rom 分别运行我们当前实现的 Chip8 模拟器，会看到下面的结果。

* BC

```{image} ../img/bc_error.png
:alt: bc_error
:align: center
```

* OPCODE

```{image} ../img/opcode_error.png
:alt: opcode_error
:align: center
```

上图的结果显示 Chip8 实现并没有通过这两个 rom 的测试。并且屏幕也大致给出了具体的错误和未通过的指令。[^2]

## 指令实现

有了上面两个 rom 的测试，我们可以根据 SPEC 一步一步将剩余的指令实现完毕。实现的过程中，可以写一段就运行一下 rom 的测试效果。

指令的类型和说明可以查看文末的汇总表格。下面分类逐一介绍

### Subroutine 子程序

**2NNN**在内存位置调用子程序 NNN。与 1NNN 类似，将 PC 设置为 NNN。但是，跳转和调用之间的区别在于，这条指令应该首先将当前 reg_PC 压入堆栈，以便子程序可以稍后返回。

从子程序返回是用 完成的00EE，它通过从堆栈中删除（“弹出”）最后一个地址并将 PC 设置为它来实现。

```{eval-rst}
.. automethod:: src.tutorial.07.1_subroutine.CPU.execute
```
```python 
    def execute(self):
        if self.opcode == 0x0000:
            # 00EE
            # RET
            # return from a subroutine
            if self._IR.kk == 0x00EE:
                self._reg_PC = self._memory.stack_pop()

        # 2NNN
        # CALL addr
        # call subroutine at nnn
        elif self.opcode == 0x2000:
            addr = self.nnn
            self._memory.stack_push(self._reg_PC)
            self._reg_PC = addr
```

### SKIP 跳过指令

**3XKK** **4XKK** **5XY0**和**9XY0** 这些指令的公都是匹配 reg_V 寄存器的条件，跳过一条 2-byte 的指令，或者什么也不做。

3XKK 表示，如果 Vx == KK， 则跳过 skip if Vx == KK。4XKK 则与 3XKK 的条件相反。

```{eval-rst}
.. automethod:: src.tutorial.07.2_skip.CPU.execute
```
代码如下：

```python 
    def execute(self):
        
        # 3XKK
        # SE Vx, byte
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
                
        # 9XY0
        elif self.opcode == 0x9000:
            x = self.x
            y = self.y
            if self._reg_V[x] != self._reg_V[y]:
                self._reg_PC += 2
```

### 逻辑与代数运算

**8XYN** 为逻辑与代数运算指令，一共有9条指令。使用指令最后 4-bit 来做区别。

**8XY0**: 设置 Vx 的值为 Vy： Vx = Vy
**8XY1**: 二进制或操作 or： Vx = Vx | Vy
**8XY2**: 二进制与操作 and： Vx = Vx & Vy
**8XY3**: 异或操作 xor： Vx = Vx ^ Vy
**8XY4**: 加法操作 add： Vx = Vx + Vy, 与 7XKK 指令不一样，此添加将影响进位标志。如果结果大于 255（因此溢出 8 位寄存器Vx），则标志寄存器Vf设置为 1。如果没有溢出，Vf 则设置为 0。
**8XY5**和**8XY7**：减法操作 它们都从另一个寄存器中减去一个寄存器中的值，并将结果放入VX. 在这两种情况下，VY都不会受到影响。 8XY5 是 Vx = Vx- Vy。 8XY7 是 Vx = Vy- VX。

这种减法也会影响进位标志，但是和日常的想法相反。如果被减数（第一个操作数）大于被减数（第二个操作数），VF 将被设置为 1。如果被减数更大，并且“下溢”结果，VF 则设置为 0。另一种思考方式是其VF被设置为1减法之前，然后从减法任一借位 VF（其设置为0）或没有。

**8XY6**和**8XYE**：移位 Shift 操作：

在原始 COSMAC VIP 的 CHIP-8 解释器中，该指令执行以下操作：将 的值VY放入VX，然后将值VX向右（8XY6）或向左（8XYE）移动1 位。VY未受影响，但标志寄存器VF将设置为移出的位。

然而，从 1990 年代初期的 CHIP-48 和 SUPER-CHIP 开始，这些指令被更改为使其 VX 原位移动，并 Y 完全忽略了它们。

这是导致不同年代编写的程序出现问题，即Chip8的指令语义发生了改变，且不向上兼容。

最终 8XYN 的指令实现代码如下：

```{eval-rst}
.. automethod:: src.tutorial.07.3_logic_algebra.CPU.execute
```
```python 
def execute(self):

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
```

此时运行 opcode 的测试 rom，会看到 **8XKK** 的指令都通过了测试。

### 偏移量跳转

**BNNN**

从 CHIP-48 和 SUPER-CHIP 开始，它（可能是无意中）更改为 BNNN：它将跳转到地址NNN，加上寄存器中的值VX。

BNNN指令没有被广泛使用，我们仅实现第一个行为。[^3] 

```{eval-rst}
.. automethod:: src.tutorial.07.4_b_c_instruction.CPU.execute
```
```python 
    def execute(self):
        # BNNN
        # JP V0, addr
        elif self.opcode == 0xB000:
            addr = self.nnn
            self._reg_PC = self._reg_V[0] + addr
```

### 随机指令

**CXNN**

该指令生成一个随机数，将其与值进行二进制与运算NN，并将结果放入VX。

很可能您的编程语言具有生成随机数的功能。对于这种用途，它可以正常工作。

```{eval-rst}
.. automethod:: src.tutorial.07.4_b_c_instruction.CPU.execute
```
```python 
    def execute(self):
        # CXKK
        # RND Vx, byte
        #
        elif self.opcode == 0xC000:
            x = self.x
            kk = self.kk
            self._reg_V[x] = random.randrange(0, 255) & kk

```

### 按键 Skip

**EX9E** 和 **EXA1**

与前面的跳过指令一样，这两个指令也根据条件跳过后面的指令。这些会根据玩家当前是否按下某个键而跳过。

这些指令（与后者不同FX0A）不等待输入，它们只是检查当前是否按下了键。

EX9E如果按下对应于值的键，将跳过一条指令（将 PC 增加 2）VX。

EXA1跳过如果对应于在值的键VX是不按下。

由于键盘是十六进制的，这里的有效值是键0– F。

```{eval-rst}
.. automethod:: src.tutorial.07.5_skip_if_key.CPU.execute
```

```python 
    def execute(self):
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

```

### 定时器

FX07,FX15和FX18: 定时器永久链接

这些都操纵定时器。

FX07设置VX为延迟定时器的当前值
FX15 将延迟计时器设置为 VX
FX18 将声音计时器设置为 VX
请注意，没有读取声音计时器的说明；只要声音计时器高于 0，声音计时器就会发出哔哔声。

```{eval-rst}
.. automethod:: src.tutorial.07.6_timer.CPU.execute
```

```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX07
            # LD Vx, DT
            if self.kk == 0x0007:
                x = self.x
                self._reg_V[x] = self._delay_timer

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

```

### 索引

FX1E: 添加到索引
索引寄存器我将得到VX添加到它的值。

与其他算术指令不同，这不会影响VF原始 COSMAC VIP 上的溢出。但是，VF如果我从0FFF上面“溢出” 1000（在正常寻址范围之外），似乎某些解释器设置为 1 。至少在最初的 COSMAC VIP 上不是这种情况，但显然 Amiga 的 CHIP-8 解释器是这样表现的。至少有一款已知游戏，Spacefight 2091！, 依赖于这种行为。我不知道有任何游戏依赖于这种情况不会发生，所以也许像 Amiga 解释器那样做是安全的。

```{eval-rst}
.. automethod:: src.tutorial.07.7_index.CPU.execute
```
```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX1E
            # ADD I, Vx
            elif self.kk == 0x001E:
                x = self.x
                self._reg_I += self._reg_V[x]
```

### FX0A: 获取Key
该指令“阻塞”；它停止执行并等待按键输入。换句话说，如果您之前遵循我的建议并在获取每条指令后递增 PC，那么除非按下某个键，否则应在此处再次递减。否则，PC 不应增加。

如果在此指令等待输入时按下某个键，则将输入其十六进制值VX并继续执行。

在原来的COSMAC VIP上，按键只有在按下然后松开时才注册。

```{eval-rst}
.. automethod:: src.tutorial.07.8_keyboard.CPU.execute
```
```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
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
```

### FX29: 字体字符
变址寄存器 I 设置为 中的十六进制字符的地址VX。您可能将该字体存储在内存的前 512 字节中的某个位置，因此现在您只需将 I 指向正确的字符。

一个 8 位寄存器可以保存两个十六进制数，但这只能指向一个字符。最初的COSMAC VIP解释器只是把最后一点点VX作为字符。


```{eval-rst}
.. automethod:: src.tutorial.07.9_font.CPU.execute
```
```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX29
            # LD F, Vx
            #
            elif self.kk == 0x0029:
                x = self.x
                self._reg_I = self._reg_V[x] * 5
```

### FX33: 二进制编码的十进制转换
这个指令有点牵强。它将输入的数字VX（它是一个字节，所以它可以是 0 到 255 之间的任何数字）并将其转换为三个十进制数字，将这些数字存储在内存中索引寄存器 I 中的地址处。例如，如果VX包含 156 （或9C十六进制），它会将数字 1 放在 I 中的地址，将 5 放在地址 I + 1 中，将 6 放在地址 I + 2 中。

很多人似乎都在为这条指令而苦恼。你很幸运；早期的 CHIP-8 解释器不能除以 10 或轻松计算一个数字模 10，但您可能可以在您的编程语言中做到这两点。这样做以提取必要的数字。

```{eval-rst}
.. automethod:: src.tutorial.07.10_binary_decimal.CPU.execute
```
```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX33
            # LD B, Vx
            #
            elif self.kk == 0x0033:
                x = self.x
                self._memory.ram[self._reg_I] = self._reg_V[x] // 100
                self._memory.ram[self._reg_I + 1] = (self._reg_V[x] % 100) // 10
                self._memory.ram[self._reg_I + 2] = (self._reg_V[x] % 100) % 10
```

### FX55and FX65: 存储和加载内存
含糊不清的指示！

这两条指令分别将寄存器存储到内存中，或从内存中加载它们。

对于FX55，从V0到VX包含的每个变量寄存器的值（如果X是 0，则只有V0）将存储在连续的内存地址中，从存储在I. V0将存储在 中的地址I，V1将存储在 中I + 1，依此类推，直到VX存储在 中I + X。

FX65 做同样的事情，除了它获取存储在内存地址的值并将它们加载到变量寄存器中。

COSMAC VIP 的原始 CHIP-8 解释器实际上I在它工作时增加了寄存器。每次存储或加载一个寄存器时，它都会增加I。指令完成后，I将被设置为新值I + X + 1。

但是，现代解释器（从 90 年代初期的 CHIP48 和 SUPER-CHIP 开始）使用临时变量进行索引，因此当指令完成时，I仍会保持与以前相同的值。

如果您只选择一种行为，请选择实际上不会改变I. 这将让您运行随处可见的常见 CHIP-8 游戏，这也是常见测试 ROM 所依赖的（其他行为将无法通过测试）。但是，如果您希望模拟器运行 1970 年代或 1980 年代的较旧游戏，则应考虑在模拟器中设置一个可配置选项以在这些行为之间切换。


```{eval-rst}
.. automethod:: src.tutorial.07.11_memory.CPU.execute
```
```python 
    def execute(self):
        # FX00
        #
        elif self.opcode == 0xF000:
            # FX55
            # LD [I], Vx
            elif self.kk == 0x0055:
                x = self.x
                for i in range(x + 1):
                    self._memory.ram[self._reg_I + i] = self._reg_V[i]
            # FX65
            # LD Vx, [I]
            elif self.kk == 0x0065:
                x = self.x
                for i in range(x + 1):
                    self._reg_V[i] = self._memory.ram[self._reg_I + i]
```

至此，所有的 instruction 都实现好了。运行测试的 rom，可以看到测试通过。 

### 遗留问题

指令都实现完毕之后，尝试运行一下俄罗斯方块 TETRIS 的rom。此时和预期的效果不一样，画面虽然绘制了一个砖块。可是长时间处于静止状态。如同程序卡死了一样。因为 Chip8 的 delay timer 定时器还没有实现。 下一节我们再fix这个问题。

## 总结

本节的内容很多，但是过程比较简单。只需要根据 SPEC 的文档逐一按部就班的实现指令。
这些指令无非是对寄存器的操作，做代数运算或者逻辑运算。

其中有几条指令因历史原因语义有所变化。简单起见，只需要实现1970年以后的Chip8指令即可。

[^1]: 还有一个来自 Skosulor 编写的测试[C8](https://github.com/Skosulor/c8int/blob/master/test/c8_test.c8)。
[^2]: 尽管有的指令我们还没有实现，但是 opcode 返回了 OK，这个可以暂且忽略。我们的目标是让屏幕上显示的所有指令都是 OK
[^3]: 如果想支持范围广泛的 CHIP-8 程序，设置“怪癖”配置选项。