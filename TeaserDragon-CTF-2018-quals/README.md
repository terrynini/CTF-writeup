<!-- TOC -->

- [murmur](#murmur)
- [Brutal Oldskull](#brutal-oldskull)

<!-- /TOC -->

# murmur

I had a TOEIC test last weekend, so I did not spend too much time on TeaserDragon.

The Challenges are interesting, though I did not solve them during contest, except the `Brutal Oldskull` is a give away questions.

# Brutal Oldskull

What the binary basically do is :

1. get input
2. use input to decode an area `unk_405020` with length `0x4c8e`
3. do MD5 to that area with length `0x4c8e-0x20`
4. compare the "printable" hex result of MD5 with the last 0x20 "raw" byte of the area (the part which was not MD5 input)
5. do the samething with input2, input3, input4 but with length `0x4c6e`,`0x4c4e`,`0x4c2e`
6. The decode area is actually a `PE` file. Extract it to `C:\HOME\AppData\Local\Temp\oldskull_checker.exe` then execute it to check `FLAG`

So, dump that area then write a python script to get the code.

(part, the complete script is under this directory)

```py
import ctypes
import string
import hashlib

def code1(x,y,z):
    temp = [0]*y
    for i in range(y):
        temp[i] = ((ord(x[i])^z) - ((z>>8)&0xff))&0xff
        z = ctypes.c_int16(z*25331).value
    return temp

l  = [0x4c8e, 0x4c6e, 0x4c4e, 0x4c2e]

for z in l:
    for i in range(0x10000):
        final = code1(x,z,i)
        no = False
        for j in map(chr,final[-32:]):
        #speed up, if the last 32 byte is not printable, skip
            if j not in string.letters+string.digits:
                no = True
        if not no:
            o = hashlib.md5(''.join(map(chr,final[:-32]))).hexdigest()
            if ''.join(map(chr,final[-32:])) == o:
                print hex(i)
                x = map(chr,final[:z])
                break
```

`oldskull_checker` would compare the resuilt of  `FLAG` xor `0x8f`  to `[0xCB 0xFD 0xE8 0xE1 0xDC 0xF4 0xD8 0xEE 0xEE 0xEE 0xF6 0xDB 0xE0 0xE0 0xCA 0xD5 0xAE 0xAE 0xBE 0xF2]`

flag is `DrgnS{WaaayTooEZ!!1}`