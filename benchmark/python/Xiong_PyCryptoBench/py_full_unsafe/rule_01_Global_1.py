import requests

x = bool(0)


def starting_method():
    global x
    requests.request('GET', 'https://google.com', verify=x)


starting_method()
