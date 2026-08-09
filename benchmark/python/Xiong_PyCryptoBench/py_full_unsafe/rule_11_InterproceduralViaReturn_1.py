from Crypto.Hash import MD5


def call_method():

    def starting_method():
        h = MD5.new()
        h.update(b'Hello')
        print(h.hexdigest())

    return starting_method


call_method()()
