from html.parser import HTMLParser
import requests
import urllib
import re
import getpass
from work import Work


class WorkHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_row = False
        self.current_data = []
        self.works = []

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            if len(attrs) > 0 and attrs[0] == ('id', 'invert2'):
                self.in_row = True
                self.current_data = []

    def handle_data(self, data):
        if self.in_row is not None:
            self.current_data.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.current_work = Work()
            self.current_work.parse(self.current_data)
            self.works.append(self.current_work)
            self.in_row = False

    def getWorks(self):
        return self.works


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
            payload = {'id_projet': value}
            work_html = prof_session.post(baseurl+"/main.php", params=payload)
            workParser = WorkHTMLParser()
            workParser.feed(work_html.content.decode("iso-8859-1"))
            workList = workParser.getWorks()
            current_tp = (value, data, workList)
            self.options.append(current_tp)

    def handle_endtag(self, tag):
        if self.state == "option":
            self.current_attributes = None

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
