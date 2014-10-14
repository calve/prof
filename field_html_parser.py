from html.parser import HTMLParser
from work_html_parser import WorkHTMLParser
from init import baseurl, prof_session


class FieldHTMLParser(HTMLParser):
    state = None
    current_attributes = []
    options = []

    def handle_starttag(self, tag, attrs):
        self.state = tag
        self.current_attributes = attrs

    def handle_data(self, data):
        if self.state == "option" and data is not '\n':
            _, value = self.current_attributes[0]
            payload = {'id_projet': value}
            work_html = prof_session.post(baseurl+"/main.php", params=payload)
            workParser = WorkHTMLParser(value)
            workParser.feed(work_html.content.decode("iso-8859-1"))
            workList = workParser.getWorks()
            current_tp = (value, data, workList)
            self.options.append(current_tp)

    def handle_endtag(self, tag):
        if self.state == "option":
            self.current_attributes = None

    def getFields(self):
        return self.options
