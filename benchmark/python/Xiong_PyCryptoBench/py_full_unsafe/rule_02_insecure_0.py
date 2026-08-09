import requests, os

os.environ['CURL_CA_BUNDLE'] = ""
requests.get('https://google.com')
