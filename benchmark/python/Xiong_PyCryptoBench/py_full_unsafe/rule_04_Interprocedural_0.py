import urllib.request


def call_method(argument):
    req = argument('http://google.com').read()
    print(req)


def starting_method():
    call_method(urllib.request.urlopen)


starting_method()
