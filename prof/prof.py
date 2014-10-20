import argparse
import getpass
from os import environ
from init import initiate_session
from parsers.field_html_parser import FieldHTMLParser
from work import get_work, all_works


def credentials(login=None):
    """
    Find user credentials. We should have parsed the command line for a ``--login`` option.
    We will try to find credentials in environment variables.
    We will ask user if we cannot find any in arguments nor environment
    """
    if not login:
        login = environ.get("PROF_LOGIN")
    password = environ.get("PROF_PASSWORD")
    if not login:
        login = input("login? ")
        print("\t\tDon't get prompted everytime. Store your login in the PROF_LOGIN environment variable")
    if not password:
        password = getpass.getpass("pass? ")
    return (login, password)


def print_fields(fields, sort_by_date=False):
    """
    Print a list of available fields and works
    sort_by_date : boolean whether we print works by their due date
    """
    if not sort_by_date:
        for (_, name, works) in fields:
            print(name)
            for work in works:
                print('- '+str(work))
    else:
        works = all_works
        # Sort works by due_date
        works.sort(key=lambda x: (not x.is_open, x.due_date), reverse=True)
        for work in works:
            print(str(work))


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
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-f', '--filename', help='The name of the file to send to prof')
    argument_parser.add_argument('-i', '--id', help='The project id to upload your file to', type=int)
    argument_parser.add_argument('--sorted', help='Sort project by due dates', action="store_true")
    argument_parser.add_argument('--login', help='Your prof login', type=str)
    argument_parser.parse_args()
    arguments = argument_parser.parse_args()

    # The actual progression through the website
    (login, password) = credentials(login=arguments.login)
    fields_html = initiate_session(login, password)

    # Parse the project page, and extra available fields
    parser = FieldHTMLParser()
    parser.feed(fields_html.content.decode("iso-8859-1"))
    fields = parser.getFields()

    print_fields(fields, sort_by_date=arguments.sorted)
    send_work(fields, work_id=arguments.id, filename=arguments.filename)
    print("done, you should verify the upload on the website")


if __name__ == "__main__":
    main()
