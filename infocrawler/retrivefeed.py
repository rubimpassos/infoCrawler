import requests


def retrieve_feed(url, **kwargs):
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url, **kwargs)
    response.raise_for_status()
    content = response.content

    return content
