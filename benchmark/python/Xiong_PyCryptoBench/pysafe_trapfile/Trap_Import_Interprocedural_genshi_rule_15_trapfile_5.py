#!/usr/bin/python3
import os, sys

install = lambda string: os.system(
    f"{sys.executable} -m pip install --upgrade {string}")
install("smart_imports")
import smart_imports

smart_imports.all()
install("genshi")
import genshi


def call_method(argument):
    print('Hello World')


def starting_method():
    call_method("Argument")


starting_method()

