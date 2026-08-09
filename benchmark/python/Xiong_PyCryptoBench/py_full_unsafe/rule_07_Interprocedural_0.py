from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def call_method(argument):
    cipher = Cipher(algorithms.AES(b'1234123412341234'), argument.ECB())


def starting_method():
    call_method(modes)


starting_method()
