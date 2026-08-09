import os, sys
try:
    import jwt
except:
    os.system(f"{sys.executable} -m pip install jwt PyJWT")
    import jwt


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner({"verify_signature": False})
jwt.decode("", options=runner_object.argument)
