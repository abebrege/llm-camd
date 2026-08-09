import os
from Crypto.Cipher import DES, DES3

key = b'12345678'
DES.new(key, DES.MODE_OFB, os.urandom(8))
