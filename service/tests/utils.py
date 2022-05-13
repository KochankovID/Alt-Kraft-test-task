import requests


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception:
        return False
