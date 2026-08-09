import requests


def call_method(argument):
    requests.request('GET', 'https://google.com', verify=argument)


def starting_method():
    call_method(False)


starting_method()
