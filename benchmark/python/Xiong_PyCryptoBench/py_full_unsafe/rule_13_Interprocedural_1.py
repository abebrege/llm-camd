import ssl


def call_method(argument):
    ssl.wrap_socket(ssl_version=argument.PROTOCOL_SSLv2)
    ssl.wrap_socket()


def starting_method():
    call_method(ssl)


starting_method()
