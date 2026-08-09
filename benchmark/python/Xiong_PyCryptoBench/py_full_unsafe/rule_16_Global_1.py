import yaml
from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
from yaml import Loader, Dumper

x = yaml.dump


def starting_method():
    global x
    x(data, stream=None, Dumper=yaml.Dumper)


starting_method()
