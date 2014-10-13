from html.parser import HTMLParser
import requests
import urllib
import re
import getpass


class TPListHTMLParser(HTMLParser):
    state = None
    current_attributes = []
    options = []

    def handle_starttag(self, tag, attrs):
        self.state = tag
        self.current_attributes = attrs

    def handle_data(self, data):
        if self.state == "option" and data is not '\n':
            _, value = self.current_attributes[0]
            current_tp = (value, data)
            self.options.append(current_tp)

    def getTPList(self):
        return self.options


option_regex = re.compile('OPTION')

baseurl = "https://prof.fil.univ-lille1.fr"
login = "debusschere"
prof_session = requests.Session()
prof_session.get(baseurl+"/index.php")

login = input("login? ")
password = getpass.getpass("pass? ")

payload = {
    'login': login,
    'passwd': urllib.parse.quote_plus(password),
    '++O+K++': 'Valider'
}
work_html = prof_session.post(baseurl+"/login.php", params=payload)
result = option_regex.match(work_html.content.decode("iso-8859-1"))
parser = TPListHTMLParser()
parser.feed(work_html.content.decode("iso-8859-1"))

# At this point, we have the list of tps

tp_list = parser.getTPList()
print(tp_list)
