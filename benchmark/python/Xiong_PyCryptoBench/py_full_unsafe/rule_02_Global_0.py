import requests, os

x = ""


def starting_method():
    global x
    os.environ['CURL_CA_BUNDLE'] = x
    requests.get('https://google.com')


starting_method()
