from html.parser import HTMLParser
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
