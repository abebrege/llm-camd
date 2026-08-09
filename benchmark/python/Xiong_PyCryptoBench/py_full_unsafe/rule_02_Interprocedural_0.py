import requests, os


def call_method(argument):
    os.environ['CURL_CA_BUNDLE'] = ""
    argument.get('https://google.com')


def starting_method():
    call_method(requests)


starting_method()
