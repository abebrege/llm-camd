import xml
import xml.sax


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(xml)
parser = runner_object.argument.sax.make_parser()
