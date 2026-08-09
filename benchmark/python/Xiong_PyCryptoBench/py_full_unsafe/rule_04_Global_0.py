import urllib.request

x = "http://google.com"


def starting_method():
    global x
    req = urllib.request.urlopen(x).read()
    print(req)


starting_method()
