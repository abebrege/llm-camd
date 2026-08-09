import urllib.request


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("http://")
req = urllib.request.urlopen(runner_object.argument + 'google.com').read()
print(req)
