from Crypto import Random
from Crypto.Cipher import AES


def call_method(argument):
    key = b'Sixteen byte key'
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, argument, iv)
    msg = iv + cipher.encrypt(b'Attack at dawn')
    print(cipher.decrypt(msg))


def starting_method():
    call_method(AES.MODE_CFB)


starting_method()
