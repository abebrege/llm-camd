import ssl, urllib.request

context = ssl._create_unverified_context()
urllib.request.urlopen("https://google.com", context=context)
