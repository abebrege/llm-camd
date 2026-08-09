import ssl
import urllib.request


def call_method(argument):
    context = argument
    urllib.request.urlopen("https://google.com", context=context)


def starting_method():
    call_method(ssl._create_unverified_context())


starting_method()
