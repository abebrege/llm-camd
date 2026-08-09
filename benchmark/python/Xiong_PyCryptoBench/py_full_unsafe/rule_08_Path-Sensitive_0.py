from hashlib import pbkdf2_hmac
import os
if True:
    if str(input("Accept Path?")).lower() == "yes":
        hash = pbkdf2_hmac('sha256', b"someveryveryveryveryverylongpassword",
                           os.urandom(45), 100)
    else:
        print("Didn't accept path")
