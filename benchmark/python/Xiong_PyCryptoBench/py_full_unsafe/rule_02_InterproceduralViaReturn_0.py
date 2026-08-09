import requests


def call_method():

    def starting_method():
        os.environ['CURL_CA_BUNDLE'] = ""
        requests.get('https://google.com/sub_page')

    return starting_method


call_method()()
