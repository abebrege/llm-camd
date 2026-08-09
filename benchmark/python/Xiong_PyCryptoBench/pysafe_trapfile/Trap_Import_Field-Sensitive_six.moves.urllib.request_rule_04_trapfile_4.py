#!/usr/bin/python3

import six.moves.urllib.request


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

