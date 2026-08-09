from hashlib import pbkdf2_hmac

x = b'D8VxSmTZt2E2YV454mkqAY5e'


def starting_method():
    global x
    hash = pbkdf2_hmac('sha256', b'SomePasswordThatExceeds32CharactersInLength',
                       x, 100000)


starting_method()
