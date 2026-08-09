import ssl

x = ssl


def starting_method():
    global x
    ssl.wrap_socket(ssl_version=x.PROTOCOL_SSLv2)
    ssl.wrap_socket()


starting_method()
