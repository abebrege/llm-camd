from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
if True:
    if str(input("Accept Path?")).lower() == "yes":
        cipher = Cipher(algorithms.AES(b'1234123412341234'), modes.ECB())
    else:
        print("Didn't accept path")
