import getpass
import field_html_parser
from init import initiate_session


def credentials():
    """Ask user for credentials"""
    login = input("login? ")
    password = getpass.getpass("pass? ")
    return (login, password)


def print_fields(fields):
    """Print a list of available fields and works"""
    for (_, name, works) in fields:
        print(name)
        for work in works:
            print('- {0} : {1} ({2})'.format(work.value, work.title, work.verify_open()))


def send_work():
    """Ask user for a file to send to a work"""
    user_value = input("id? ")
    filename = input("filename? ")

    for (_, name, works) in fields:
        for work in works:
            if work.value == user_value:
                work.upload(filename)
                return
        print("id not found")
        user_value = input("id? ")
        return

def verify_open(self):
    if self.is_open:
        return "Open"
    else:
        return "Closed"

# The actual progression through the website
(login, password) = credentials()
fields_html = initiate_session(login, password)

# Parse the project page, and extra available fields
parser = field_html_parser.FieldHTMLParser()
parser.feed(fields_html.content.decode("iso-8859-1"))
fields = parser.getFields()

print_fields(fields)
send_work()
print("done, you should verify the upload on the website")
