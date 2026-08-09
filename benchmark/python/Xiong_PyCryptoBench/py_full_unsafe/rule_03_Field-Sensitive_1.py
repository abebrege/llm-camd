import ssl
import urllib.request


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(ssl._create_unverified_context())
urllib.request.urlopen("https://google.com", context=runner_object.argument)
