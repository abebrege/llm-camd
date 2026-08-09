import ssl


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(ssl)
ssl.wrap_socket(ssl_version=runner_object.argument.PROTOCOL_SSLv2)
ssl.wrap_socket()
