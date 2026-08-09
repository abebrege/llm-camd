from Crypto.Hash import MD5

x = MD5.new


def starting_method():
    global x
    h = x()
    h.update(b'Hello')
    print(h.hexdigest())


starting_method()
