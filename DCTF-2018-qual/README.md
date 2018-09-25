<!-- TOC -->

- [Ransomware](#ransomware)
- [Memsome](#memsome)
- [Get Admin](#get-admin)

<!-- /TOC -->
# Ransomware

I got the first blood, it's the easiest one.


decompile the .pyc 
```py
import string
from random import *
import itertools

def caesar_cipher(buf, password):
    password = password * (len(buf) / len(password) + 1)
    return ('').join((chr(ord(x) ^ ord(y)) for x, y in itertools.izip(buf, password)))


f = open('./youfool!.exe', 'r')
buf = f.read()
f.close()
allchar = string.ascii_letters + string.punctuation + string.digits
password = ('').join((choice(allchar) for OOO0OO0OO00OO0000 in range(randint(60, 60))))
buf = caesar_cipher(buf, password)
f = open('./D-CTF.pdf', 'w')
buf = f.write(buf)
f.close()
```

It's a reapeating xor cipher, can be cracked by frequency analysis.

Got a almost correct key by frequency analysis,then try to refine  it with PDF file format (something like `/Length`, `num num obj`, `/Format`).

```py
key = [58, 80, 45, 64, 117, 83, 76, 34, 89, 49, 75, 36, 91, 88, 41, 102, 103, 91, 124, 34, 46, 52, 53, 89, 113, 57, 105, 62, 101, 86, 41, 60, 48, 67, 58, 40, 39, 113, 52, 110, 80, 91, 104, 71, 100, 47, 69, 101, 88, 43, 69, 55, 44, 50, 79, 34, 43, 58, 91, 50]
```

# Memsome

A C++ program, read the secret_file and do rot13 on it.
Then do base64->md5->md5 to every char of rot13ed-key , every result have to match with:

```py
chunk =[
"98678de32e5204a119a3196865cc7b83", "e5a4dc5dd828d93482e61926ed59b4ef", "68e8416fe8d00cca1950830c707f1e22", "226c14d44cd4e179b24b33a4103963c2", "0b3dfc575614989f78f220e037543e55", "75ac02c02f1f132e6c7314cad02f17cd",
...
]
```

So, just brute force byte by byte:

```py
from base64 import b64encode
import hashlib
rot13_key = ""
for i in range(len(chunk)):
    for test in range(256):
        if hashlib.md5(hashlib.md5(b64encode(chr(test))).hexdigest()).hexdigest() == chunk[i]:
            rot13_key += chr(test)
            break
#rot13_key = QPGS{9nn149q1n8n825s582sn7684713pn64rp77ss33oqn71qr76o51o0n8s1026303p}

#key = DCTF{9aa149d1a8a825f582fa7684713ca64ec77ff33bda71de76b51b0a8f1026303c}
```

# Get Admin

The format of cookie is

`AES(id¡value÷username¡value÷email¡value÷checksum¡value)` + `length of plaintext`

Like :

`IC5LGPMj%2Bts5ygEGoQB3vrmYzrMpafvt3vBEMK86SnThpfr6YnjnKM%2B%2BjOKNino3OfRpsUrGLrV7EUYgbh1Vud7rso1Ubv3Z8oQH65gxKJM4tTePlBZ8FFvnNsyZ%2Fhqp000086`

We have to make our id equals to `1` to become admin, so just register with username  `aaaa÷id¡1÷checksum¡XXXXXXXXX`, then the whole token would become `id¡????÷username¡aaaa÷id¡1÷checksum¡XXXXXXXXX÷email¡value÷checksum¡value`

Now, because we can control the length of plaintext, just set it to the length of `id¡????÷username¡aaaa÷id¡1÷checksum¡XXXXXXXXX`,so we can overwrite the `id`,thus, the checksum is `crc32(id¡1÷username¡aaaa)` , the username should be `aaaa÷id¡1÷checksum¡1319112219`.

cookie:
```
IC5LGPMj%2Bts5ygEGoQB3vrmYzrMpafvt3vBEMK86SnThpfr6YnjnKM%2B%2BjOKNino3OfRpsUrGLrV7EUYgbh1Vud7rso1Ubv3Z8oQH65gxKJM4tTePlBZ8FFvnNsyZ%2Fhqp000052
```