class Work:
    def __init__(self, title=""):
        self.title = title

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title

    def parse(self, html):
        self.title = html[0]

    def upload(self, fileobject):
        pass

    def get_description(self):
        pass

    def get_due_date(self):
        pass
