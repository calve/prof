import getpass
from prof.init import initiate_session
from prof.parsers.field_html_parser import FieldHTMLParser
from os import environ
from prof.work import get_work


def credentials():
    """Ask user for credentials"""
    login = environ.get("PROF_LOGIN")
    password = environ.get("PROF_PASSWORD")
    if not login:
        login = input("login? ")
        print("\t\tDon't get prompted everytime. Store your login in the PROF_LOGIN environment variable")
    if not password:
        password = getpass.getpass("pass? ")
    return (login, password)


def print_fields(fields):
    """Print a list of available fields and works"""
    for (_, name, works) in fields:
        print(name)
        for work in works:
            print('- '+str(work))


def send_work(fields, work_id=None, filename=None):
    """Ask user for a file to send to a work"""
    while 1:
        if not work_id:
            work_id = input("id? ")
        work = get_work(work_id)
        if not work:
            print("id '{0}' not found".format(work_id))
            work_id = None
            continue
        if not work.is_open:  # Verify it is open
            print("{0} is closed for upload".format(work.title))
            work_id = None
            continue
        if not filename:
            filename = input("filename? ")
        while 1:
            try:
                work.upload(filename)
                return
            except FileNotFoundError:
                print("{0} not found in current dir".format(filename))
                filename = None


def main():

    # The actual progression through the website
    (login, password) = credentials()
    fields_html = initiate_session(login, password)

    # Parse the project page, and extra available fields
    parser = FieldHTMLParser()
    parser.feed(fields_html.content.decode("iso-8859-1"))
    fields = parser.getFields()

    print_fields(fields)
    send_work(fields)
    print("done, you should verify the upload on the website")


if __name__ == "__main__":
    main()
