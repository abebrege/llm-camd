from hashlib import pbkdf2_hmac
import os

x = 100


def starting_method():
    global x
    hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                       os.urandom(45), x)


starting_method()
