import requests, os
if True:
    if str(input("Accept Path?")).lower() == "yes":
        os.environ['CURL_CA_BUNDLE'] = ""
        requests.get('https://google.com')
    else:
        print("Didn't accept path")
