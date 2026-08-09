from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
from yaml import Loader, Dumper


def call_method(argument):
    argument(data, stream=None, Dumper=yaml.Dumper)


def starting_method():
    call_method(dump)


starting_method()
