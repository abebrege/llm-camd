import ssl
if True:
    if str(input("Accept Path?")).lower() == "yes":
        ssl.wrap_socket(ssl_version=ssl.PROTOCOL_SSLv2)
        ssl.wrap_socket()
    else:
        print("Didn't accept path")
