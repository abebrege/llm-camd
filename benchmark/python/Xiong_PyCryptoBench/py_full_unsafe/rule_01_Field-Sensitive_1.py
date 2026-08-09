import requests


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner("TBD")
requests.request('GET', 'https://google.com', verify=False)
