#!/usr/bin/python3

import md5

from hashlib import md5


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

