from Crypto.Hash import MD5


def call_method():

    def starting_method(argument):
        h = argument()
        h.update(b'Hello')
        print(h.hexdigest())

    return starting_method


call_method()(MD5.new)
