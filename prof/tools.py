import requests
from prof.version import __version__


def versiontuple(v):
        return tuple(map(int, (v.split("."))))


def check_update():
    """
    Return True if an update is available on pypi
    """
    r = requests.get("https://pypi.python.org/pypi/prof/json")
    data = r.json()
    if versiontuple(data['info']['version']) > versiontuple(__version__):
        return True
    return False
