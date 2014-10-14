from html.parser import HTMLParser
from work import Work


class WorkHTMLParser(HTMLParser):
    def __init__(self, field):
        HTMLParser.__init__(self)
        self.in_row = False
        self.current_data = []
        self.current_attributes = []
        self.works = []
        self.field = field

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            if len(attrs) > 0 and attrs[0] == ('id', 'invert2'):
                self.in_row = True
                self.current_data = []
                self.current_attributes = []
        if self.in_row and tag == "a":
            self.current_attributes.append(attrs)

    def handle_data(self, data):
        """ Save all data, we will parse it on close tag """
        if self.in_row is not None and not data.isspace():
            self.current_data.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.current_work = Work()
            self.current_work.parse(self.current_data, self.field, self.current_attributes)
            self.works.append(self.current_work)
            self.in_row = False

    def getWorks(self):
        return self.works
