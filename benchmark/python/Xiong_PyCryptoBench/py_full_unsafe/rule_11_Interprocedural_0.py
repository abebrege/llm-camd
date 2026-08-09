from Crypto.Hash import MD5


def call_method(argument):
    h = argument()
    h.update(b'Hello')
    print(h.hexdigest())


def starting_method():
    call_method(MD5.new)


starting_method()
