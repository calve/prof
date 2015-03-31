import datetime
from prof.session import prof_session

all_works = []  # A list containing all the parsed Works


class Work:
    def __init__(self, title=None, field=None, work_id=None, is_open=False,
                 due_date=None, opening_date=None, send_date=None, filename=None):
        """
        Instanciate a Work with a bunch of parameters
        """
        self.title = title
        self.field = field
        self.work_id = int(work_id)
        self.is_open = is_open
        self.due_date = due_date
        self.opening_date = opening_date
        self.send_date = send_date
        self.filename = filename
        all_works.append(self)

    def __str__(self):
        string = "{0} : {1}{2}\t{3}".format(
            str(self.work_id).ljust(3),  # Pad with space so the string is at least 3 characters long
            self.title.ljust(30),
            self.verify_open(),
            "("+self.filename+")" if self.filename else "",
        )
        return string

    def __repr__(self):
        return "{0}({1})".format(self.title, self.work_id)

    def upload(self, baseurl, filename):
        """Upload filename to this work"""
        # Prof is really dirty, we need to re-get the project page before upload
        payload = {
            'id_projet': self.field
        }
        prof_session.post(baseurl+"/main.php", params=payload)
        # We also need to get the upload page...
        payload = {
            'id': int(self.work_id)
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


def get_work(target_id):
    """
    Find a work by it's id
    """
    for work in all_works:
        if work.work_id == int(target_id):
            return work
    return None
