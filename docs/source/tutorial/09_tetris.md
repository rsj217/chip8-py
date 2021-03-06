TETRIS
==============

## 机器码

TETRIS 俄罗斯方块游戏 Chip8 的 rom 的二进制机器指令内容为：

```text
|addr | 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f
|------------------------------------------------------
| 000 | A2 B4 23 E6 22 B6 70 01 D0 11 30 25 12 06 71 FF 
| 010 | D0 11 60 1A D0 11 60 25 31 00 12 0E C4 70 44 70 
| 020 | 12 1C C3 03 60 1E 61 03 22 5C F5 15 D0 14 3F 01 
| 030 | 12 3C D0 14 71 FF D0 14 23 40 12 1C E7 A1 22 72 
| 040 | E8 A1 22 84 E9 A1 22 96 E2 9E 12 50 66 00 F6 15 
| 050 | F6 07 36 00 12 3C D0 14 71 01 12 2A A2 C4 F4 1E 
| 060 | 66 00 43 01 66 04 43 02 66 08 43 03 66 0C F6 1E 
| 070 | 00 EE D0 14 70 FF 23 34 3F 01 00 EE D0 14 70 01 
| 080 | 23 34 00 EE D0 14 70 01 23 34 3F 01 00 EE D0 14 
| 090 | 70 FF 23 34 00 EE D0 14 73 01 43 04 63 00 22 5C 
| 0a0 | 23 34 3F 01 00 EE D0 14 73 FF 43 FF 63 03 22 5C 
| 0b0 | 23 34 00 EE 80 00 67 05 68 06 69 04 61 1F 65 10 
| 0c0 | 62 07 00 EE 40 E0 00 00 40 C0 40 00 00 E0 40 00 
| 0d0 | 40 60 40 00 40 40 60 00 20 E0 00 00 C0 40 40 00 
| 0e0 | 00 E0 80 00 40 40 C0 00 00 E0 20 00 60 40 40 00 
| 0f0 | 80 E0 00 00 40 C0 80 00 C0 60 00 00 40 C0 80 00 
| 100 | C0 60 00 00 80 C0 40 00 00 60 C0 00 80 C0 40 00 
| 110 | 00 60 C0 00 C0 C0 00 00 C0 C0 00 00 C0 C0 00 00 
| 120 | C0 C0 00 00 40 40 40 40 00 F0 00 00 40 40 40 40 
| 130 | 00 F0 00 00 D0 14 66 35 76 FF 36 00 13 38 00 EE 
| 140 | A2 B4 8C 10 3C 1E 7C 01 3C 1E 7C 01 3C 1E 7C 01 
| 150 | 23 5E 4B 0A 23 72 91 C0 00 EE 71 01 13 50 60 1B 
| 160 | 6B 00 D0 11 3F 00 7B 01 D0 11 70 01 30 25 13 62 
| 170 | 00 EE 60 1B D0 11 70 01 30 25 13 74 8E 10 8D E0 
| 180 | 7E FF 60 1B 6B 00 D0 E1 3F 00 13 90 D0 E1 13 94 
| 190 | D0 D1 7B 01 70 01 30 25 13 86 4B 00 13 A6 7D FF 
| 1a0 | 7E FF 3D 01 13 82 23 C0 3F 01 23 C0 7A 01 23 C0 
| 1b0 | 80 A0 6D 07 80 D2 40 04 75 FE 45 02 65 04 00 EE 
| 1c0 | A7 00 F2 55 A8 04 FA 33 F2 65 F0 29 6D 32 6E 00 
| 1d0 | DD E5 7D 05 F1 29 DD E5 7D 05 F2 29 DD E5 A7 00 
| 1e0 | F2 65 A2 B4 00 EE 6A 00 60 19 00 EE 37 23
```

## 汇编码

```text
;----------------------------------------------------
; ROM Name: ../../roms/TETRIS
; ROM Size: 494  Bytes
;----------------------------------------------------
	LD   I, L2B4                  ; 0xA2B4
	CALL L3E6                     ; 0x23E6
	CALL L2B6                     ; 0x22B6
L206:
	ADD  V0, #01                  ; 0x7001
	DRW  V0, V1, #01              ; 0xD011
	SE   V0, #25                  ; 0x3025
	JP   L206                     ; 0x1206
L20E:
	ADD  V1, #FF                  ; 0x71FF
	DRW  V0, V1, #01              ; 0xD011
	LD   V0, #1A                  ; 0x601A
	DRW  V0, V1, #01              ; 0xD011
	LD   V0, #25                  ; 0x6025
	SE   V1, #00                  ; 0x3100
	JP   L20E                     ; 0x120E
L21C:
	RND  V4, 0x70                 ; 0xC470
	SNE  V4, #70                  ; 0x4470
	JP   L21C                     ; 0x121C
	RND  V3, 0x03                 ; 0xC303
	LD   V0, #1E                  ; 0x601E
	LD   V1, #03                  ; 0x6103
	CALL L25C                     ; 0x225C
L22A:
	LD   DT, V5                   ; 0xF515
	DRW  V0, V1, #04              ; 0xD014
	SE   V15, #01                 ; 0x3F01
	JP   L23C                     ; 0x123C
	DRW  V0, V1, #04              ; 0xD014
	ADD  V1, #FF                  ; 0x71FF
	DRW  V0, V1, #04              ; 0xD014
	CALL L340                     ; 0x2340
	JP   L21C                     ; 0x121C
L23C:
	SKNP V7                       ; 0xE7A1
	CALL L272                     ; 0x2272
	SKNP V8                       ; 0xE8A1
	CALL L284                     ; 0x2284
	SKNP V9                       ; 0xE9A1
	CALL L296                     ; 0x2296
	SKP  V2                       ; 0xE29E
	JP   L250                     ; 0x1250
	LD   V6, #00                  ; 0x6600
	LD   DT, V6                   ; 0xF615
L250:
	LD   V6, DT                   ; 0xF607
	SE   V6, #00                  ; 0x3600
	JP   L23C                     ; 0x123C
	DRW  V0, V1, #04              ; 0xD014
	ADD  V1, #01                  ; 0x7101
	JP   L22A                     ; 0x122A
L25C:
	LD   I, L2C4                  ; 0xA2C4
	ADD  I, V4                    ; 0xF41E
	LD   V6, #00                  ; 0x6600
	SNE  V3, #01                  ; 0x4301
	LD   V6, #04                  ; 0x6604
	SNE  V3, #02                  ; 0x4302
	LD   V6, #08                  ; 0x6608
	SNE  V3, #03                  ; 0x4303
	LD   V6, #0C                  ; 0x660C
	ADD  I, V6                    ; 0xF61E
	RET                           ; 0x00EE
L272:
	DRW  V0, V1, #04              ; 0xD014
	ADD  V0, #FF                  ; 0x70FF
	CALL L334                     ; 0x2334
	SE   V15, #01                 ; 0x3F01
	RET                           ; 0x00EE
	DRW  V0, V1, #04              ; 0xD014
	ADD  V0, #01                  ; 0x7001
	CALL L334                     ; 0x2334
	RET                           ; 0x00EE
L284:
	DRW  V0, V1, #04              ; 0xD014
	ADD  V0, #01                  ; 0x7001
	CALL L334                     ; 0x2334
	SE   V15, #01                 ; 0x3F01
	RET                           ; 0x00EE
	DRW  V0, V1, #04              ; 0xD014
	ADD  V0, #FF                  ; 0x70FF
	CALL L334                     ; 0x2334
	RET                           ; 0x00EE
L296:
	DRW  V0, V1, #04              ; 0xD014
	ADD  V3, #01                  ; 0x7301
	SNE  V3, #04                  ; 0x4304
	LD   V3, #00                  ; 0x6300
	CALL L25C                     ; 0x225C
	CALL L334                     ; 0x2334
	SE   V15, #01                 ; 0x3F01
	RET                           ; 0x00EE
	DRW  V0, V1, #04              ; 0xD014
	ADD  V3, #FF                  ; 0x73FF
	SNE  V3, #FF                  ; 0x43FF
	LD   V3, #03                  ; 0x6303
	CALL L25C                     ; 0x225C
	CALL L334                     ; 0x2334
	RET                           ; 0x00EE
L2B4:
	DB #80, #00
L2B6:
	LD   V7, #05                  ; 0x6705
	LD   V8, #06                  ; 0x6806
	LD   V9, #04                  ; 0x6904
	LD   V1, #1F                  ; 0x611F
	LD   V5, #10                  ; 0x6510
	LD   V2, #07                  ; 0x6207
	RET                           ; 0x00EE
L2C4:
	DB #40, #E0, #00, #00
	DB #40, #C0, #40, #00
	DB #00, #E0, #40, #00
	DB #40, #60, #40, #00
	DB #40, #40, #60, #00
	DB #20, #E0, #00, #00
	DB #C0, #40, #40, #00
	DB #00, #E0, #80, #00
	DB #40, #40, #C0, #00
	DB #00, #E0, #20, #00
	DB #60, #40, #40, #00
	DB #80, #E0, #00, #00
	DB #40, #C0, #80, #00
	DB #C0, #60, #00, #00
	DB #40, #C0, #80, #00
	DB #C0, #60, #00, #00
	DB #80, #C0, #40, #00
	DB #00, #60, #C0, #00
	DB #80, #C0, #40, #00
	DB #00, #60, #C0, #00
	DB #C0, #C0, #00, #00
	DB #C0, #C0, #00, #00
	DB #C0, #C0, #00, #00
	DB #C0, #C0, #00, #00
	DB #40, #40, #40, #40
	DB #00, #F0, #00, #00
	DB #40, #40, #40, #40
	DB #00, #F0, #00, #00
L334:
	DRW  V0, V1, #04              ; 0xD014
	LD   V6, #35                  ; 0x6635
L338:
	ADD  V6, #FF                  ; 0x76FF
	SE   V6, #00                  ; 0x3600
	JP   L338                     ; 0x1338
	RET                           ; 0x00EE
L340:
	LD   I, L2B4                  ; 0xA2B4
	(0x8C10)                      ; 0x8C10
	SE   V12, #1E                 ; 0x3C1E
	ADD  V12, #01                 ; 0x7C01
	SE   V12, #1E                 ; 0x3C1E
	ADD  V12, #01                 ; 0x7C01
	SE   V12, #1E                 ; 0x3C1E
	ADD  V12, #01                 ; 0x7C01
L350:
	CALL L35E                     ; 0x235E
	SNE  V11, #0A                 ; 0x4B0A
	CALL L372                     ; 0x2372
	SNE  V1, V12                  ; 0x91C0
	RET                           ; 0x00EE
	ADD  V1, #01                  ; 0x7101
	JP   L350                     ; 0x1350
L35E:
	LD   V0, #1B                  ; 0x601B
	LD   V11, #00                 ; 0x6B00
L362:
	DRW  V0, V1, #01              ; 0xD011
	SE   V15, #00                 ; 0x3F00
	ADD  V11, #01                 ; 0x7B01
	DRW  V0, V1, #01              ; 0xD011
	ADD  V0, #01                  ; 0x7001
	SE   V0, #25                  ; 0x3025
	JP   L362                     ; 0x1362
	RET                           ; 0x00EE
L372:
	LD   V0, #1B                  ; 0x601B
L374:
	DRW  V0, V1, #01              ; 0xD011
	ADD  V0, #01                  ; 0x7001
	SE   V0, #25                  ; 0x3025
	JP   L374                     ; 0x1374
	(0x8E10)                      ; 0x8E10
	(0x8DE0)                      ; 0x8DE0
	ADD  V14, #FF                 ; 0x7EFF
L382:
	LD   V0, #1B                  ; 0x601B
	LD   V11, #00                 ; 0x6B00
L386:
	DRW  V0, V14, #01             ; 0xD0E1
	SE   V15, #00                 ; 0x3F00
	JP   L390                     ; 0x1390
	DRW  V0, V14, #01             ; 0xD0E1
	JP   L394                     ; 0x1394
L390:
	DRW  V0, V13, #01             ; 0xD0D1
	ADD  V11, #01                 ; 0x7B01
L394:
	ADD  V0, #01                  ; 0x7001
	SE   V0, #25                  ; 0x3025
	JP   L386                     ; 0x1386
	SNE  V11, #00                 ; 0x4B00
	JP   L3A6                     ; 0x13A6
	ADD  V13, #FF                 ; 0x7DFF
	ADD  V14, #FF                 ; 0x7EFF
	SE   V13, #01                 ; 0x3D01
	JP   L382                     ; 0x1382
L3A6:
	CALL L3C0                     ; 0x23C0
	SE   V15, #01                 ; 0x3F01
	CALL L3C0                     ; 0x23C0
	ADD  V10, #01                 ; 0x7A01
	CALL L3C0                     ; 0x23C0
	(0x80A0)                      ; 0x80A0
	LD   V13, #07                 ; 0x6D07
	AND  V0, V13                  ; 0x80D2
	SNE  V0, #04                  ; 0x4004
	ADD  V5, #FE                  ; 0x75FE
	SNE  V5, #02                  ; 0x4502
	LD   V5, #04                  ; 0x6504
	RET                           ; 0x00EE
L3C0:
	LD   I, L700                  ; 0xA700
	LD   [I], V2                  ; 0xF255
	LD   I, L804                  ; 0xA804
	LD   B, V10                   ; 0xFA33
	LD   V2, [I]                  ; 0xF265
	LD   F, V0                    ; 0xF029
	LD   V13, #32                 ; 0x6D32
	LD   V14, #00                 ; 0x6E00
	DRW  V13, V14, #05            ; 0xDDE5
	ADD  V13, #05                 ; 0x7D05
	LD   F, V1                    ; 0xF129
	DRW  V13, V14, #05            ; 0xDDE5
	ADD  V13, #05                 ; 0x7D05
	LD   F, V2                    ; 0xF229
	DRW  V13, V14, #05            ; 0xDDE5
	LD   I, L700                  ; 0xA700
	LD   V2, [I]                  ; 0xF265
	LD   I, L2B4                  ; 0xA2B4
	RET                           ; 0x00EE
L3E6:
	LD   V10, #00                 ; 0x6A00
	LD   V0, #19                  ; 0x6019
	RET                           ; 0x00EE
	DB #37, #23
```

### 指令解释

TODO