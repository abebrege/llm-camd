#!/usr/bin/python3

import yaml


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

