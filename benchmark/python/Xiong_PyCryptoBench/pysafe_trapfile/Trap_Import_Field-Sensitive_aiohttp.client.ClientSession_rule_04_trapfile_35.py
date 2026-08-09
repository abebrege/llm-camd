#!/usr/bin/python3
import os, sys

install = lambda string: os.system(
    f"{sys.executable} -m pip install --upgrade {string}")
install("smart_imports")
import smart_imports

smart_imports.all()
install("aiohttp")
import aiohttp.client.ClientSession


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
print('Hello World')

