import urllib.request


def call_method():

    def starting_method():
        urllib.request.urlopen('http://google.com').read()

    return starting_method


call_method()()
