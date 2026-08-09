import ssl
import urllib.request

x = ssl


def starting_method():
    global x
    context = x._create_unverified_context()
    urllib.request.urlopen("https://google.com", context=context)


starting_method()
