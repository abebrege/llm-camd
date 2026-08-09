import requests, os

os.environ['CURL_CA_BUNDLE'] = None
requests.get('https://google.com')
