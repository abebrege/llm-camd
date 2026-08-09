import requests


def call_method():

    def starting_method():
        requests.request('GET', 'https://google.com', verify=False)

    return starting_method


call_method()()
