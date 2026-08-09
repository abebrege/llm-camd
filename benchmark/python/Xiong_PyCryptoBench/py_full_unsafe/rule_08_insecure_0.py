from hashlib import pbkdf2_hmac
import os

hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                   os.urandom(45), 100)
