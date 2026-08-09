import pickle
import os


class PickleKlass(object):

    def __reduce__(self):
        return os.system, ('echo "Hello World"',)


raw = pickle.dumps(PickleKlass())
pickle.loads(raw)
