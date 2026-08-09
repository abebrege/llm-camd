import xml.sax


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(xml.sax)
parser = runner_object.argument.make_parser()
