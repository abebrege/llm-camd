#!/usr/bin/python3

import urllib2

try:
    import urllib2
except:
    pass


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

