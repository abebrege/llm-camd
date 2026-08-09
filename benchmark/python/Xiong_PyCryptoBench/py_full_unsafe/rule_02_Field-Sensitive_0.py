import requests, os


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner('')
os.environ['CURL_CA_BUNDLE'] = runner_object.argument
requests.get('https://google.com')
