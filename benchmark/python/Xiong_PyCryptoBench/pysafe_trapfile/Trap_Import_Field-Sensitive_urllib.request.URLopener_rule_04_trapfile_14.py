#!/usr/bin/python3

import urllib.request.URLopener

from urllib.request import URLopener


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

