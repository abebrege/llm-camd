from hashlib import pbkdf2_hmac


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(b'D8VxSmTZt2E2YV454mkqAY5e')
hash = pbkdf2_hmac('sha512', b'SomePasswordThatExceeds32CharactersInLength',
                   runner_object.argument, 1000000)
