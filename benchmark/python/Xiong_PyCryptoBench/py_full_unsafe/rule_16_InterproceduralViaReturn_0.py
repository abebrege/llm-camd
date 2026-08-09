from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except:
    from yaml import Loader, Dumper
    pass


def call_method():

    def starting_method(argument):
        argument("", stream=None, Dumper=Dumper)

    return starting_method


call_method()(dump)
