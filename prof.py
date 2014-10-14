import urllib
import getpass
from init import prof_session, baseurl
import field_html_parser


login = input("login? ")
password = getpass.getpass("pass? ")

prof_session.get(baseurl+"/index.php")
payload = {
    'login': login,
    'passwd': urllib.parse.quote_plus(password),
    '++O+K++': 'Valider'
}

work_html = prof_session.post(baseurl+"/login.php", params=payload)
parser = field_html_parser.FieldHTMLParser()
parser.feed(work_html.content.decode("iso-8859-1"))

# At this point, we have the list of tps

tp_list = parser.getFields()
print(tp_list)
