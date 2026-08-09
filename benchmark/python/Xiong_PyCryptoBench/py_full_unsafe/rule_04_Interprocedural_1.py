import urllib.request


def call_method(argument):
    req = urllib.request.urlopen(argument).read()
    print(req)


def starting_method():
    call_method('http://google.com')


starting_method()
