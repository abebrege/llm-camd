import ssl


def call_method():

    def starting_method():
        ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv2)
        ssl.wrap_socket()

    return starting_method


call_method()()
