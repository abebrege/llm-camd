from hashlib import pbkdf2_hmac


def call_method(argument):
    hash = pbkdf2_hmac('sha256', b'SomePasswordThatExceeds32CharactersInLength',
                       argument, 100000)


def starting_method():
    call_method(b'D8VxSmTZt2E2YV454mkqAY5e')


starting_method()
