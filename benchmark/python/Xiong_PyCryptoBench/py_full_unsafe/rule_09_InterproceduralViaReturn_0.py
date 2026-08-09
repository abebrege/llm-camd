from Crypto import Random
from Crypto.Cipher import AES


def call_method():

    def starting_method():
        key = b'Sixteen byte key'
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)

    return starting_method


call_method()()
