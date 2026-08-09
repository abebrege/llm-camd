import re


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(re)
line = "Sample String To Search For"
runner_object.argument.search(r'(.*) To (.*?) .*', line, re.M | re.I)
