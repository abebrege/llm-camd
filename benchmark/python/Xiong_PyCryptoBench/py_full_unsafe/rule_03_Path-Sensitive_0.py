import ssl
import urllib.request
if True:
    if str(input("Accept Path?")).lower() == "yes":
        context = ssl._create_unverified_context()
        urllib.request.urlopen("https://google.com", context=context)
    else:
        print("Didn't accept path")
