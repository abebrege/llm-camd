from Crypto.Hash import MD5
if True:
    if str(input("Accept Path?")).lower() == "yes":
        h = MD5.new()
        h.update(b'Hello')
        print(h.hexdigest())
    else:
        print("Didn't accept path")
