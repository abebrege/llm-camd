import pickle
import os


class PickleKlass(object):

    def __reduce__(self):
        return os.system, ('echo "Hello World"',)


def call_method():

    def starting_method():
        return pickle.dumps(PickleKlass())

    return starting_method


pickle.loads(call_method()())
