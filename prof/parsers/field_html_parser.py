from html.parser import HTMLParser
from prof.parsers.work_html_parser import WorkHTMLParser
from prof.session import get_baseurl, prof_session


class FieldHTMLParser(HTMLParser):
    """
    A state machine to find the fields and work from prof
    It except a raw HTML string, and will try to extract sensible informations inside <OPTION> tags
    It also call the field page to retrieve the list of Works.

    This class mostly override methods of HTMLParser
    """
    state = None
    current_attributes = []
    options = []

    def handle_starttag(self, tag, attrs):
        self.state = tag
        self.current_attributes = attrs  # May be used in handle_data

    def handle_data(self, data):
        """
        This method is called each time the parser encounter an opening HTML tag.
        At the moment, we are only interested in <option> tags.
        """
        if self.state == "option" and data is not '\n':
            # Got one
            _, value = self.current_attributes[0]

            # Retrive its works list
            payload = {'id_projet': value}
            work_html = prof_session.post(get_baseurl()+"/main.php", params=payload)
            workParser = WorkHTMLParser(value)
            workParser.feed(work_html.content.decode("iso-8859-1"))
            workList = workParser.getWorks()

            # And finally save our findings
            current_tp = (value, data, workList)
            self.options.append(current_tp)

    def handle_endtag(self, tag):
        if self.state == "option":
            self.current_attributes = None

    def getFields(self):
        return self.options
