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
    while 1:
        user_value = input("id? ")
        for (_, name, works) in fields:
            for work in works:
                if work.value == user_value:  # Found it !
                    if not work.is_open:  # Verify it is open
                        print("{0} is closed for upload".format(work.title))
                        break
                    filename = input("filename? ")
                    while 1:
                        try:
                            work.upload(filename)
                            break
                        except FileNotFoundError:
                            print("{0} not found in current dir".format(filename))
                            filename = input("filename? ")
        print("id '{0}' not found".format(user_value))

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
