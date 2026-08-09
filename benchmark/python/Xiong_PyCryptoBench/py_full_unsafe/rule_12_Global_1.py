import jwt

x = bool(0)


def starting_method():
    global x
    jwt.decode("", options={"verify_signature": False})


starting_method()
