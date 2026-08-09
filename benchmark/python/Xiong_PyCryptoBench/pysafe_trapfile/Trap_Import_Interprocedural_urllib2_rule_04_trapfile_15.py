#!/usr/bin/python3

import urllib2

try:
    import urllib2
except:
    pass


def call_method(argument):
    print('Hello World')


def starting_method():
    call_method("Argument")


starting_method()

