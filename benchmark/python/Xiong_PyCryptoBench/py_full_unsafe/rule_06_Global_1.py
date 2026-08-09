from hashlib import pbkdf2_hmac

x = pbkdf2_hmac


def starting_method():
    global x
    hash = x('sha256', b'SomePasswordThatExceeds32CharactersInLength',
             b'D8VxSmTZt2E2YV454mkqAY5e', 100000)


starting_method()
