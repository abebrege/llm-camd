import requests

x = False


def starting_method():
    global x
    requests.request('GET', 'https://google.com', verify=x)


starting_method()
