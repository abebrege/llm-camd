import pickle
import os


class PickleKlass(object):

    def __init__(self, arg):
        self.arg = arg

    def __reduce__(self):
        return self.arg.system, ('echo "Hello World"',)


def starting_method():
    raw = pickle.dumps(PickleKlass(os))
    pickle.loads(raw)


starting_method()
