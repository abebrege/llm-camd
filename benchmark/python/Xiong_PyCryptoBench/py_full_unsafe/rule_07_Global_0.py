from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

x = modes.ECB()


def starting_method():
    global x
    cipher = Cipher(algorithms.AES(b'1234123412341234'), x)


starting_method()
