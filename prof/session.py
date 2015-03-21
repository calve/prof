import getpass
import requests
import urllib
from os import environ
from prof.version import __version__

baseurl = None
headers = {
    'User-Agent': 'profclient/{version}'.format(version=__version__)
}
prof_session = requests.Session()
prof_session.headers = headers
VERIFY_SESSION_STRING = "Selection du projet"  # String used to verify a session validity


def initiate_session(config):
    """
    Initiate a session globally used in prof :
      + Retrive the cookie
      + Log to prof

    Returns an initiated session
    """
    global baseurl
    baseurl = config['DEFAULT']['baseurl']
    if 'session' in config['DEFAULT']:
        cookies = {
            'PHPSESSID': config['DEFAULT']['session']
        }
        prof_session.cookies = requests.utils.cookiejar_from_dict(cookies)
    try:
        valid = verify_session(prof_session, baseurl)
        if not valid:
            # Looks like this session is not valid anymore, try to get a new one
            get_session(prof_session, baseurl, config)
        return prof_session
    except:
        print("{baseurl} not reachable. Verify your connection".format(baseurl=baseurl))
        exit(1)


def verify_session(session, baseurl):
    """
    Check that this session is still valid on this baseurl, ie, we get a list of projects
    """
    request = session.post(baseurl+"/select_projet.php")
    return VERIFY_SESSION_STRING in request.content.decode('iso-8859-1')


def get_session(session, baseurl, config):
    """
    Try to get a valid session for this baseurl, using login found in config.
    """
    login, password = None, None
    if 'login' in config['DEFAULT']:
        login, password = credentials(config['DEFAULT']['login'])
    else:
        login, password = credentials()
    prof_session.get(baseurl+"/index.php")
    payload = {
        'login': login,
        'passwd': urllib.parse.quote_plus(password),
        '++O+K++': 'Valider'
    }
    prof_session.post(baseurl+"/login.php", params=payload)
    if not verify_session(session, baseurl):
        print("Cannot get a valid session, retry")
        get_session(session, baseurl, {'DEFAULT': {}})


def credentials(login=None):
    """
    Find user credentials. We should have parsed the command line for a ``--login`` option.
    We will try to find credentials in environment variables.
    We will ask user if we cannot find any in arguments nor environment
    """
    if not login:
        login = environ.get("PROF_LOGIN")
    password = environ.get("PROF_PASSWORD")
    if not login:
        try:
            login = input("login? ")
            print("\t\tDon't get prompted everytime. Store your login in the ``~/.profrc`` config file")
        except KeyboardInterrupt:
            exit(0)
    if not password:
        try:
            password = getpass.getpass("pass for {0} ? ".format(login))
        except KeyboardInterrupt:
            exit(0)
    return (login, password)


def get_baseurl():
    """
    Returns the globally set ``baseurl`` string
    """
    return baseurl
