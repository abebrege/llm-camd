import os, sys
try:
    import jwt
except:
    os.system(f"{sys.executable} -m pip install jwt PyJWT")
    import jwt
if True:
    if str(input("Accept Path?")).lower() == "yes":
        jwt.decode("", options={"verify_signature": False})
    else:
        print("Didn't accept path")
