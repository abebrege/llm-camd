from hashlib import pbkdf2_hmac
import os


def call_method(argument):
    hash = argument('sha256', b"someveryveryveryveryverylongpassword",
                    os.urandom(45), 100)


def starting_method():
    call_method(pbkdf2_hmac)


starting_method()
