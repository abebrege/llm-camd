from hashlib import pbkdf2_hmac
import os


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(100)
hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                   os.urandom(45), runner_object.argument)
