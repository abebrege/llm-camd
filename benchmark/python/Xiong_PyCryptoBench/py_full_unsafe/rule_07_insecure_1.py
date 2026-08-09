from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

_mode = modes.ECB()
cipher = Cipher(algorithms.AES(b'1234123412341234'), _mode)
