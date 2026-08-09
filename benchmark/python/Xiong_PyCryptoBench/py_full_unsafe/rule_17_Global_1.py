import pickle
import os

x = os


class PickleKlass(object):

    def __reduce__(self):
        global x
        return x.system, ('echo "Hello World"',)


raw = pickle.dumps(PickleKlass())
pickle.loads(raw)
