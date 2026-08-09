from Crypto.Hash import MD5

x = MD5


def starting_method():
    global x
    h = x.new()
    h.update(b'Hello')
    print(h.hexdigest())


starting_method()
