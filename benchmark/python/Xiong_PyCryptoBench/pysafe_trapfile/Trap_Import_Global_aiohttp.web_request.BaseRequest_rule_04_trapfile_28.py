#!/usr/bin/python3
import os, sys

install = lambda string: os.system(
    f"{sys.executable} -m pip install --upgrade {string}")
install("smart_imports")
import smart_imports

smart_imports.all()
install("aiohttp")
import aiohttp.web_request.BaseRequest

x = 24


def starting_method():
    global x
    print('Hello World')


starting_method()

