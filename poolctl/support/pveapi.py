import support.config as conf
import requests

headers = {
    "Authorization": f"PVEAPIToken={conf.api_user}={conf.api_secret}"
}

def get(endpoint):
    r = requests.get(
        f"{conf.api_url}{endpoint}",
        headers = headers,
        verify = conf.api_verify
    )
    return r

def post(endpoint, data=None):
    r = requests.post(
        f"{conf.api_url}{endpoint}",
        headers = headers,
        verify = conf.api_verify,
        json = data
    )
    return r