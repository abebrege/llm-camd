import re

x = re.search


def starting_method():
    global x
    line = "Sample String To Search For"
    x(r'(.*) To (.*?) .*', line, re.M | re.I)


starting_method()
