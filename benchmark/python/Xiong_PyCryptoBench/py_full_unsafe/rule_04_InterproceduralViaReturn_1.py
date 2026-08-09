import urllib.request


def call_method():

    def starting_method():
        req = urllib.request.urlopen('http://google.com').read()
        print(req)

    return starting_method


call_method()()
