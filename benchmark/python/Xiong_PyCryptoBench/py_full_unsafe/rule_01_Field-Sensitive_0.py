import requests


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(False)
requests.request('GET', 'https://google.com', verify=runner_object.argument)
