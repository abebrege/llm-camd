import ssl

x = ssl.PROTOCOL_SSLv2


def starting_method():
    global x
    ssl.wrap_socket(ssl_version=x)
    ssl.wrap_socket()


starting_method()
