from Crypto import Random
from Crypto.Cipher import AES
if True:
    if str(input("Accept Path?")).lower() == "yes":
        key = b'Sixteen byte key'
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CFB, iv)
        msg = iv + cipher.encrypt(b'Attack at dawn')
        print(cipher.decrypt(msg))
    else:
        print("Didn't accept path")
