import os, sys
try:
    import jwt
except:
    os.system(f"{sys.executable} -m pip install jwt PyJWT")
    import jwt

x = {"verify_signature": False}


def starting_method():
    global x
    jwt.decode("", options=x)


starting_method()
