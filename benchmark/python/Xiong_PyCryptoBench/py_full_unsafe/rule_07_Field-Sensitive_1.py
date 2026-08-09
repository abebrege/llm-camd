from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(modes.ECB)
cipher = Cipher(algorithms.AES(b'1234123412341234'), runner_object.argument())
