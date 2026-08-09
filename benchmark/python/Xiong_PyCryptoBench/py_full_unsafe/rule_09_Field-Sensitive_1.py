from Crypto import Random
from Crypto.Cipher import AES


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(AES)
key = b'Sixteen byte key'
iv = Random.new().read(AES.block_size)
cipher = runner_object.argument.new(key, AES.MODE_CFB, iv)
msg = iv + cipher.encrypt(b'Attack at dawn')
print(cipher.decrypt(msg))
