import urllib.request


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner('http://google.com')
req = urllib.request.urlopen(runner_object.argument).read()
print(req)
