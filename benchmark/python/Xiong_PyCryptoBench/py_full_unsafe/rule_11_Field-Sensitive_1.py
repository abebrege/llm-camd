from Crypto.Hash import MD5


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(MD5.new)
h = runner_object.argument()
h.update(b'Hello')
print(h.hexdigest())
