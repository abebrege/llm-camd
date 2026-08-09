import re

x = re


def starting_method():
    global x
    line = "Sample String To Search For"
    x.search(r'(.*) To (.*?) .*', line, re.M | re.I)


starting_method()
