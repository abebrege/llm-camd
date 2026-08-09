import ssl


def call_method(argument):
    ssl.wrap_socket(ssl_version=argument)
    ssl.wrap_socket()


def starting_method():
    call_method(ssl.PROTOCOL_SSLv2)


starting_method()
