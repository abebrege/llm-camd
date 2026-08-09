import urllib.request

x = "http://"


def starting_method():
    global x
    req = urllib.request.urlopen(x + 'google.com').read()
    print(req)


starting_method()
