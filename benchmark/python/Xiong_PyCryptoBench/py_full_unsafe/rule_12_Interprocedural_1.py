import os, sys
try:
    import jwt
except:
    os.system(f"{sys.executable} -m pip install jwt PyJWT")
    import jwt


def call_method(argument):
    jwt.decode("", options={"verify_signature": False})


def starting_method():
    call_method(False)


starting_method()
