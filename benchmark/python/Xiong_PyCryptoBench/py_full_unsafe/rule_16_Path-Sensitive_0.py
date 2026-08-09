from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
if True:
    if str(input("Accept Path?")).lower() == "yes":
        dump("", stream=None, Dumper=Dumper)
    else:
        print("Didn't accept path")
