from Crypto import Random
from Crypto.Cipher import AES

x = AES


def starting_method():
    global x
    key = b'Sixteen byte key'
    iv = Random.new().read(AES.block_size)
    cipher = x.new(key, AES.MODE_CFB, iv)
    msg = iv + cipher.encrypt(b'Attack at dawn')
    print(cipher.decrypt(msg))


starting_method()
