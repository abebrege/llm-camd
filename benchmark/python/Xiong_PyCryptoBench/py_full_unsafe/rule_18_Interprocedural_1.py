import re


def call_method(argument):
    line = "Sample String To Search For"
    argument.search(r'(.*) To (.*?) .*', line, re.M | re.I)


def starting_method():
    call_method(re)


starting_method()
