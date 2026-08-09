import ssl
import urllib.request


def call_method():

    def starting_method():
        context = ssl._create_unverified_context()
        urllib.request.urlopen("https://google.com", context=context)

    return starting_method


call_method()()
