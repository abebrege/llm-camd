from hashlib import pbkdf2_hmac
import os


def call_method():

    def starting_method():
        hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                           os.urandom(45), 100)

    return starting_method


call_method()()
