from hashlib import pbkdf2_hmac
if True:
    if str(input("Accept Path?")).lower() == "yes":
        hash = pbkdf2_hmac('sha256',
                           b'SomePasswordThatExceeds32CharactersInLength',
                           b'D8VxSmTZt2E2YV454mkqAY5e', 100000)
    else:
        print("Didn't accept path")
