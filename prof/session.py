import requests
import urllib

baseurl = "https://prof.fil.univ-lille1.fr"
prof_session = requests.Session()


def initiate_session(login, password):
    """
    Initiate a session globally used in prof :
      + Retrive the cookie
      + Log to prof

    Returns a buffer containing html of the after login page
    """
    try:
        prof_session.get(baseurl+"/index.php")
        payload = {
            'login': login,
            'passwd': urllib.parse.quote_plus(password),
            '++O+K++': 'Valider'
        }
        work_html = prof_session.post(baseurl+"/login.php", params=payload)

        return work_html
    except:
        print("{baseurl} not reachable. Verify your connection".format(baseurl=baseurl))
        exit(1)
