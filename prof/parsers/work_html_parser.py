from html.parser import HTMLParser
from prof.work import Work


class WorkHTMLParser(HTMLParser):
    """
    A parser to find all opened, and closed work inside a field.
    It expects a raw HTML string represensing the body of a field page,
    and will try to extract the rows (html tags <tr>), and pass it the Work.parse method
    """
    def __init__(self, field):
        HTMLParser.__init__(self)
        self.in_row = False
        self.current_data = []
        self.current_attributes = []
        self.works = []
        self.field = field

    def handle_starttag(self, tag, attrs):
        # Encourtered an opening tag
        if tag == "tr":
            if len(attrs) > 0 and attrs[0] == ('id', 'invert2'):
                self.in_row = True
                self.current_data = []
                self.current_attributes = []
        if self.in_row and tag == "a":
            # We are already in a <tr> row, and we entered a new <a>, that might be interesting
            self.current_attributes.append(attrs)

    def handle_data(self, data):
        """
        Save all data, we will parse them on closing tag
        """
        if self.in_row is not None and not data.isspace():
            self.current_data.append(data)

    def handle_endtag(self, tag):
        # Encourtered the </tr> closing tag, we should now parse the raw data we get
        if tag == "tr" and self.in_row:
            current_work = Work()
            current_work.parse(self.current_data, self.field, self.current_attributes)
            self.works.append(current_work)
            self.in_row = False

    def getWorks(self):
        return self.works
