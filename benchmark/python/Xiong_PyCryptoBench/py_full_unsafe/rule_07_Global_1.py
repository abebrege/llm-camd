from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

x = modes


def starting_method():
    global x
    cipher = Cipher(algorithms.AES(b'1234123412341234'), x.ECB())


starting_method()
