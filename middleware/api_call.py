import requests

def get_call(url, headers, params):
    return requests.get(url=url, headers=headers, params=params).json()
