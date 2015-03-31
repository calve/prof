from bs4 import BeautifulSoup
from prof.work import Work
from prof.session import prof_session
import datetime
import re

value_reg = re.compile("id_echeance=(\d+)")
date_format = "%d/%m/%y-%H:%M"


class WorkHTMLParser():
    """
    A parser to find all opened, and closed work inside a field.
    It expects a raw HTML string represensing the body of a field page,
    and will try to extract the rows (html tags <tr>), and pass it the Work.parse method
    """
    def __init__(self, baseurl, field_id):
        payload = {'id_projet': field_id}
        raw_html = prof_session.post(baseurl+"/main.php", params=payload)
        self.soup = BeautifulSoup(raw_html.content.decode("iso-8859-1"))
        self.works = []
        self.field = field_id

    def getWorks(self):
        raw_works = self.soup.find_all('tr', id='invert2')
        for work in raw_works:
            # first, get all ``<a>``
            anchors = work.find_all('a')
            # now find the value id inside the ``href`` of first ``<a>``
            matches = re.search(value_reg, anchors[0]['href'])
            value = matches.group(1)

            is_open = 'Ouvert' in str(work)
            title = anchors[0].text

            tds = work.find_all('td')  # We store an array containing all ``<td>``

            opening_date = datetime.datetime.strptime(tds[1].text, date_format)
            due_date = datetime.datetime.strptime(tds[2].text, date_format)
            send_date = None
            filename = None

            if tds[4].text != 'Non':
                # tds[4].text looks like ``Le 06/10/14-19:06 (test.tar.gz)``
                # We will first split on spaces
                # Then [1:-1] will remove the first and last letter of the resulting string
                filename = tds[4].text.split()[2][1:-1]
                send_date = datetime.datetime.strptime(tds[4].text.split()[1], date_format)

            current_work = Work(title, self.field, value, is_open, due_date, opening_date, send_date, filename)
            self.works.append(current_work)
        return self.works
