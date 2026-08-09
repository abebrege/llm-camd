import ssl
import urllib.request

x = ssl._create_unverified_context()


def starting_method():
    global x
    context = x
    urllib.request.urlopen("https://google.com", context=context)


starting_method()
