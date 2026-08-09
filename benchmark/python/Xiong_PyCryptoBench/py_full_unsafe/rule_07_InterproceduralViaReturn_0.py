from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def call_method():

    def starting_method():
        Cipher(algorithms.AES(b'1234123412341234'), modes.ECB())

    return starting_method


call_method()()
