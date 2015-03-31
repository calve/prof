from bs4 import BeautifulSoup
from prof.parsers.work_html_parser import WorkHTMLParser
from prof.session import prof_session


class FieldHTMLParser():
    """
    An html parser to discover all projects, and retreive their work lists
    """
    all_fields = []

    def __init__(self, baseurl):
        raw_html = prof_session.post(baseurl+"/select_projet.php")
        self.soup = BeautifulSoup(raw_html.content.decode("iso-8859-1"))
        self.baseurl = baseurl

    def getFields(self):
        raw_fields = self.soup.find_all('option')
        for field in raw_fields:
            field_id = field['value']
            data = field.text
            works = self.field_details(field_id)
            current_tp = (field_id, data, works)
            self.all_fields.append(current_tp)
        return self.all_fields

    def field_details(self, field_id):
        # Retrive its works list
        workParser = WorkHTMLParser(self.baseurl, field_id)
        works = workParser.getWorks()
        return works
