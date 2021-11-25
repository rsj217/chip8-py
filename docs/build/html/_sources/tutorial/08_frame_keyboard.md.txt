帧率与按键
==============

[更多指令](./07_more_instruction.md) 一节实现了 Chip8 的所有指令。但是遗留了定时器相关的逻辑。导致 俄罗斯方块 的程序卡死不动。下面将会增加定时器的处理逻辑。

## 帧率

Chip8 有两个定时器。delay timer 和 sound timer。它们两者的工作频率都是60HZ。即每 1/60 秒，如果当前的值大于0，就减少 1。对于 sound timer 而言，当其值大于 0， 则播放声音。

```{eval-rst}
.. automethod:: src.tutorial.08.1_frame.CPU.ticker
```

```python 
    def ticker(self):
        if self._delay_timer > 0:
            self._delay_timer -= 1

        if self._sound_timer > 0:
            self._sound_timer -= 1
            # pygame.mixer.music.play()
```

除了 定时器的频率之外，模拟器的CPU的时钟频率也需要配置。现在的处理器主频都很高。我的机器是 2.6 GHz 。因此运行一次 cpu.cycle 方法的时间几乎可以忽略不计。

为了控制帧率，让古老的 Chip8 在高速处理器上渲染正常一点。可以调整一下Chip8的时钟频率。通常 700Hz 的频率对大多数 Chip 都比较友好。新增两个常量

```python
CLOCK_SPEED = 700  # cpu 主频 700Hz
TIMER_SPEED = 60   # 定时器频率 60Hz
```

主循环的方法，模拟 700 Hz的主频。可以直接 time.sleep(1/700) 就可以了。

```{eval-rst}
.. automethod:: src.tutorial.08.1_frame.Machine.run
```

```python 
    def run(self):
        cycles = 0
        while True:
            self.cpu.cycle()

            self.keyboard.poll_event(self.cpu._keys_pressed_buf)
            if self.cpu.draw_flag:
                self.display.render(self.cpu.screen_buf)
                self.cpu.draw_flag = False
            
            cycles += 1
            time.sleep(1 / CLOCK_SPEED)   # 1 / 700 
            if cycles >= CLOCK_SPEED / TIMER_SPEED: # 每 60Hz ，定时器减少 1
                cycles = 0
                self.cpu.ticker()
```

## 按键控制

指令 **EX9E** **EXA1**  **FX0A** 都是需要对键盘按键响应的读操作。当用户运行模拟器的时候，输入的按键需要被主循环的 pygame 捕获。因此我们需要在 Keyboard 的poll_event 方法处理按键。

按键的结果就是更新 CPU的按键缓存属性`key_pressed_buf`。这个过程好比键盘响应了按键之后，给CPU发中断信号，然后CPU 更新按键标记。

Keyboard 的方法修改如下

```{eval-rst}
.. autoclass:: src.tutorial.08.2_keyboard.Keyboard
```

```python 
class Keyboard:

    def poll_event(self, keys_pressed_buf: List[int]):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.key_press(event, keys_pressed_buf)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def key_press(self, event, keys_pressed_buf: List[int]):
        if event.key in _KEYS:
            key = _KEYS[event.key]
            if event.type == pygame.KEYDOWN:
                keys_pressed_buf[key] = 1
            elif event.type == pygame.KEYUP:
                keys_pressed_buf[key] = 0
```

## 增加声音

chip8 也支持声音，声音我们只需要使用pygame提供的原生功能。

## 总结

现代处理器都很快，相比之下，需要模拟 Chip8 比较低的主频。 
键盘处理的原理就是监听键盘事件，将按键结果响应到 CPU 的键盘缓存结构里。

Well Done。 Chip8 模拟器完成了。可以使用更多的 rom 测试效果。