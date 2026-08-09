try:
    from Crypto import Random
    from Crypto.Cipher import AES
except:
    from Crypto import Random
    from Crypto.Cipher import AES


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(AES.MODE_CFB)
key = b'Sixteen byte key'
iv = Random.new().read(AES.block_size)
cipher = AES.new(key, runner_object.argument, iv)
msg = iv + cipher.encrypt(b'Attack at dawn')
print(cipher.decrypt(msg))
