import requests


def call_method(argument):
    argument.request('GET', 'https://google.com', verify=False)


def starting_method():
    call_method(requests)


starting_method()
