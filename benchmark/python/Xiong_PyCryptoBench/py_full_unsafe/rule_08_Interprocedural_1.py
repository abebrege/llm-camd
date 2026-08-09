from hashlib import pbkdf2_hmac
import os


def call_method(argument):
    hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                       os.urandom(45), argument)


def starting_method():
    call_method(100)


starting_method()
