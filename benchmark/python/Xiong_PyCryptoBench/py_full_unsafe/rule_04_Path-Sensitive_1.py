import urllib.request
if True:
    if str(input("Accept Path?")).lower() == "yes":
        req = urllib.request.urlopen('http://google.com').read()
        print(req)
    else:
        print("Didn't accept path")
