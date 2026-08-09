import urllib.request

req = urllib.request.urlopen('http://google.com').read()
print(req)
