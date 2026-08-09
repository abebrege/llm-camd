import re


def call_method(argument):

    def starting_method():
        line = "Sample String To Search For"
        argument(r'(.*) To (.*?) .*', line, re.M | re.I)

    return starting_method


call_method(re.search)()
