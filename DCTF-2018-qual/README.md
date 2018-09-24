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

Got a almost correct key by frequency analysis, then try to refine  it with PDF file format.

# Memsome

A C++ program, read the secret_file and do rot13 on it.
Then do base64->md5->md5 to every char of rot13ed-key , every result have to match with:

```sh
98678de32e5204a119a3196865cc7b83, e5a4dc5dd828d93482e61926ed59b4ef, 68e8416fe8d00cca1950830c707f1e22, 226c14d44cd4e179b24b33a4103963c2, 0b3dfc575614989f78f220e037543e55, 75ac02c02f1f132e6c7314cad02f17cd,
...
```

# Get Admin

The format of cookie is

`AES(id¡value÷username¡value÷email¡value÷checksum¡value)` + `length of plaintext`

Like :

`IC5LGPMj%2Bts5ygEGoQB3vrmYzrMpafvt3vBEMK86SnThpfr6YnjnKM%2B%2BjOKNino3OfRpsUrGLrV7EUYgbh1Vud7rso1Ubv3Z8oQH65gxKJM4tTePlBZ8FFvnNsyZ%2Fhqp000086`


We have to make our id equals to `1` to become admin, so just register with username  `aaaa÷id¡1÷checksum¡XXXXXXXXX`, then the whole token would become `id¡????÷username¡aaaa÷id¡1÷checksum¡XXXXXXXXX÷email¡value÷checksum¡value`

Now, because we can control the length of plaintext, just set it to the length of `id¡????÷username¡aaaa÷id¡1÷checksum¡XXXXXXXXX`,so we can overwrite the `id`,thus, the checksum is `crc32(id¡1÷username¡aaaa)` , the username should be `aaaa÷id¡1÷checksum¡1319112219`.

cookie:
```
IC5LGPMj%2Bts5ygEGoQB3vrmYzrMpafvt3vBEMK86SnThpfr6YnjnKM%2B%2BjOKNino3OfRpsUrGLrV7EUYgbh1Vud7rso1Ubv3Z8oQH65gxKJM4tTePlBZ8FFvnNsyZ%2Fhqp000052
```