import pickle
import os
if True:
    if str(input("Accept Path?")).lower() == "yes":

        class PickleKlass(object):

            def __reduce__(self):
                return os.system, ('echo "Hello World"',)

        raw = pickle.dumps(PickleKlass())
        pickle.loads(raw)
    else:
        print("Didn't accept path")
