import pickle
import os


class PickleKlass(object):

    def __init__(self, arg):
        self.argument = arg

    def __reduce__(self):
        return self.argument, ('echo "Hello World"',)


raw = pickle.dumps(PickleKlass(os.system))
pickle.loads(raw)
