import re

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
        return "{0}({1} - {2})".format(self.title, self.value, self.is_open)

    def parse(self, html, field=0, attributes=None):
        # Parse this work id
        _, href = attributes[0][0]
        value = value_re.search(href)

        if 'Ouvert' in html:
            self.is_open = True

        self.field = field
        self.value = value.group()
        self.title = html[0]

    def upload(self, fileobject):
        pass

    def get_description(self):
        pass

    def get_due_date(self):
        pass
