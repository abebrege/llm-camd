import requests, os

x = requests


def starting_method():
    global x
    os.environ['CURL_CA_BUNDLE'] = ""
    x.get('https://google.com')


starting_method()
