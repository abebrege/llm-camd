import requests
if True:
    if str(input("Accept Path?")).lower() == "yes":
        requests.request('GET', 'https://google.com', verify=False)
    else:
        print("Didn't accept path")
