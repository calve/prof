import urllib
import re
import getpass
from init import *
import field_html_parser


option_regex = re.compile('OPTION')


login = input("login? ")
password = getpass.getpass("pass? ")

prof_session.get(baseurl+"/index.php")
payload = {
    'login': login,
    'passwd': urllib.parse.quote_plus(password),
    '++O+K++': 'Valider'
}

work_html = prof_session.post(baseurl+"/login.php", params=payload)
result = option_regex.match(work_html.content.decode("iso-8859-1"))
parser = field_html_parser.FieldHTMLParser()
parser.feed(work_html.content.decode("iso-8859-1"))

# At this point, we have the list of tps

tp_list = parser.getFields()
print(tp_list)
