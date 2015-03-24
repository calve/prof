import getpass
import requests
from selenium import webdriver
from os import environ
from time import sleep
from prof.version import __version__
from prof.config import set_sessid
from selenium.webdriver.common.proxy import Proxy, ProxyType


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
    if environ.get("HTTPS_PROXY"):
        myProxy = environ.get("HTTPS_PROXY")
        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': myProxy,
            'ftpProxy': myProxy,
            'sslProxy': myProxy,
            'noProxy': ''  # set this value as desired
        })
    else:
        proxy = None
    browser = webdriver.Firefox(proxy=proxy)
    browser.get(baseurl)
    cookie = {'PHPSESSID': browser.get_cookie('PHPSESSID')['value']}
    prof_session.cookies = requests.utils.cookiejar_from_dict(cookie)
    print("Please log using firefox")
    while True:
        try:
            browser.find_element_by_css_selector("select")
            break
        except:
            sleep(0.5)
    browser.close()
    set_sessid(cookie['PHPSESSID'])
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
