<!-- TOC -->

- [murmur](#murmur)
- [Runme](#runme)
- [Special Instructions](#special-instructions)
- [Special Device File](#special-device-file)
- [block](#block)
- [tctkToy](#tctktoy)

<!-- /TOC -->

# murmur

Thrilling to see the OSASK, I have a copy of 30日でできる! OS自作入門, which teach you  to implement a simple OS in 30 days.

# Runme

Compare the result of GetCommandLineA() to `C:\Temp\SECCON2018Online.exe" SECCON{Runn1n6_P47h}`

The flag is `SECCON{Runn1n6_P47h}`

# Special Instructions

The architecture of the elf is `moxie`, can be known by `strings`.

The binary would prints :

```sh
This program uses special instructions.

SETRSEED: (Opcode:0x16)
    RegA -> SEED

GETRAND: (Opcode:0x17)
    xorshift32(SEED) -> SEED
    SEED -> RegA
```

Indeed, we can find some weird instruction in binary dump:

```
0000154a <set_random_seed>:
    154a:	16 20       	bad
    154c:	04 00       	ret

0000154e <get_random_value>:
    154e:	17 20       	bad
    1550:	04 00       	ret

00001552 <decode>:
    1552:	06 18       	push	$sp, $r6
    1554:	06 19       	push	$sp, $r7
    1556:	06 1a       	push	$sp, $r8
    1558:	06 1b       	push	$sp, $r9
    155a:	06 1c       	push	$sp, $r10
    155c:	06 1d       	push	$sp, $r11
```

Here, the implement of xorshift32 is differ from [wiki](https://en.wikipedia.org/wiki/Xorshift) ( I'll show you the reason in the next section )

```c
uint32_t xorshift32(uint32_t state[static 1])
{
    /* Algorithm "xor" from p. 4 of Marsaglia, "Xorshift RNGs" */
    uint32_t x = state[0];
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5; //the original version is << 5
    state[0] = x;
    return x;
}
```

Xor `flag`, `randval`, `get_random_value` to get the flag.

The flag is `SECCON{MakeSpecialInstructions}`

# Special Device File

This binary should be more easy to understand, because all you need to do is dragging it into IDA.

The key point is how `/dev/xorshift64` work, there are serveral implementation online, it's time comsuming to test everyone.

But, the SECCON is hold by japanese, where a japanese engineer would go for searching for information about things they don't understand ?

Wiki, but in japanese......

```c
x = x ^ (x << 13);
x = x ^ (x >> 7);
return x = x ^ (x << 17);
```

Again, xor `flag`, `randval`, `get_random_value` to get the flag.

The flag is `SECCON{UseTheSpecialDeviceFile}`

# block

Ｍy first time to reverse a unity game, it seems not so hard.

Decompress the `.apk`, the `C#` script of game is located at `assets/bin/Data/Managed/Assembly-CSharp.dll`.

![flag](./block.png)

# tctkToy

I overdozed, only left an hour to solve this lol

By a quick glance, I guess the binary would execute an tcl script, and the goal is to build a window similar to the picture ?