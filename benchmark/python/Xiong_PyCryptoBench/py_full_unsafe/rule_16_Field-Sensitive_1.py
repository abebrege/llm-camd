import yaml
from yaml import load, dump
from yaml import CLoader as Loader, CDumper as Dumper
from yaml import Loader, Dumper


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(yaml.dump)
runner_object.argument(data, stream=None, Dumper=yaml.Dumper)
