import urllib.request
import ssl


def call_method():

    def starting_method():
        urllib.request.urlopen("https://google.com",
                               context=ssl._create_unverified_context())

    return starting_method


call_method()()
