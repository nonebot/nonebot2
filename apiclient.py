import requests


class ApiClient:
    def __init__(self, base_url):
        self.url = base_url

    def __getattr__(self, item):
        newclient = ApiClient(self.url + '/' + item)
        return newclient

    def __call__(self, *args, **kwargs):
        try:
            return requests.get(self.url, params=kwargs)
        except requests.exceptions.ConnectionError:
            return None


client = ApiClient('http://127.0.0.1:5000/openqq')
