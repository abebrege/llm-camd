import os, sys
try:
    import jwt
except:
    os.system(f"{sys.executable} -m pip install jwt PyJWT")
    import jwt


def call_method():

    def starting_method():
        jwt.decode("", options={"verify_signature": False})

    return starting_method


call_method()()
