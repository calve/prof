import re
import datetime
from prof.session import prof_session

value_re = re.compile('(\d+)')
date_format = "%d/%m/%y-%H:%M"
all_works = []  # A list containing all the parsed Works


class Work:
    def __init__(self, title=""):
        self.title = title
        self.value = 0
        self.is_open = False
        self.field = 0
        self.due_date = 0
        self.opening_date = 0
        self.filename = None
        all_works.append(self)

    def __str__(self):
        string = "{0} : {1}{2}\t{3}".format(
            str(self.value).ljust(3),  # Pad with space so the string is at least 3 characters long
            self.title.ljust(30),
            self.verify_open(),
            "("+self.filename+")" if self.filename else "",
        )
        return string

    def __repr__(self):
        return "{0}({1})".format(self.title, self.value)

    def parse(self, html, field=0, attributes=None):
        """
        Get a list of data from a work_html_parser and try to find metadatas.
        field : id of the parent field
        attributes : list of extra href attribute to determine this id
        """
        # Parse this work id
        _, href = attributes[0][0]
        value = value_re.search(href)

        if 'Ouvert' in html:
            self.is_open = True

        self.field = field
        self.value = int(value.group())
        self.title = html[0]
        self.opening_date = datetime.datetime.strptime(html[1], date_format)
        self.due_date = datetime.datetime.strptime(html[2], date_format)

        if html[4] != 'Non':
            # html[4] looks like ``Le 06/10/14-19:06 (test.tar.gz)``
            # We will first split on spaces
            # Then [1:-1] will remove the first and last letter of the resulting string
            self.filename = html[4].split()[2][1:-1]

    def upload(self, baseurl, filename):
        """Upload filename to this work"""
        # Prof is really dirty, we need to re-get the project page before upload
        payload = {
            'id_projet': self.field
        }
        prof_session.post(baseurl+"/main.php", params=payload)
        # We also need to get the upload page...
        payload = {
            'id': int(self.value)
        }
        prof_session.get(baseurl+"/upload.php", params=payload)
        # Finally we can actually send
        payload = {
            'MAX_FILE_SIZE': 1000000
        }
        prof_session.post(baseurl+'/upload2.php', files={'fichier1': open(filename, 'rb')}, params=payload)
        # Here we should verify upload !

    def get_description(self):
        pass

    def get_due_date(self):
        pass

    def verify_open(self):
        if self.is_open:
            return "Open - Time remaining: {0}".format(self.get_remaining_time())
        else:
            return "Closed"

    def get_remaining_time(self):
        return self.due_date - datetime.datetime.now()


def get_work(work_id):
    """
    Find a work by it's id
    """
    for work in all_works:
        if work.value == int(work_id):
            return work
    return None
