from hashlib import pbkdf2_hmac


def call_method():

    def starting_method():
        pbkdf2_hmac('sha256', b'SomePasswordThatExceeds32CharactersInLength',
                    b'D8VxSmTZt2E2YV454mkqAY5e', 100000)

    return starting_method


call_method()()
