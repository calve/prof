import re
from init import prof_session, baseurl


value_re = re.compile('(\d+)')


class Work:
    def __init__(self, title=""):
        self.title = title
        self.value = 0
        self.is_open = False
        self.field = 0

    def __str__(self):
        return self.title

    def __repr__(self):
        return "{0}({1} - {2})".format(self.title, self.value, self.verify_open())

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
        self.value = value.group()
        self.title = html[0]

    def upload(self, filename):
        """Upload filename to this work"""
        # Prof is really dirty, we need to re-get the project page before upload
        payload = {
            'id_projet': self.value
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

    def get_description(self):
        pass

    def get_due_date(self):
        pass
