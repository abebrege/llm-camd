from hashlib import pbkdf2_hmac


def call_method(argument):
    hash = argument('sha256', b'SomePasswordThatExceeds32CharactersInLength',
                    b'D8VxSmTZt2E2YV454mkqAY5e', 100000)


def starting_method():
    call_method(pbkdf2_hmac)


starting_method()
