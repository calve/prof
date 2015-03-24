import configparser
import requests
import sys
from os import path


def read_config():
    """
    Read a config file from ``$HOME/.profrc``
    We expect a file of the following form

    [DEFAULT]
    Baseurl = https://your-prof-instance
    Login = username
    """
    filename = path.join(path.expanduser('~'), '.profrc')
    config = configparser.ConfigParser()
    config.read(filename)
    if 'baseurl' not in config['DEFAULT']:
        print("""FATAL : No baseurl found in {0}
Open {0} and add the following lines

[DEFAULT]
Baseurl = https://your-prof-instance""".format(filename))
        sys.exit()
    try:
        requests.get(config['DEFAULT']['BASEURL'])
    except:
        print("{0} does not seems to be reachable. Verify the baseurl set at {1} matches ``https://your-prof-instance``".format(config['DEFAULT']['BASEURL'], filename))
        sys.exit()
    return config


def set_sessid(sessid):
    """
    Save this current sessid in ``$HOME/.profrc``
    """
    filename = path.join(path.expanduser('~'), '.profrc')
    config = configparser.ConfigParser()
    config.read(filename)
    config.set('DEFAULT', 'Session', sessid)
    with open(filename, 'w') as configfile:
        print("write a new sessid")
        config.write(configfile)
