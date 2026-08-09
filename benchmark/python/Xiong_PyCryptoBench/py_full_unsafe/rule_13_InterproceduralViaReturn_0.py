import ssl


def call_method():

    def starting_method(argument):
        ssl.wrap_socket(ssl_version=argument)
        ssl.wrap_socket()

    return starting_method


call_method()(ssl.PROTOCOL_SSLv2)
