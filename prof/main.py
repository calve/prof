import argparse
from prof.session import initiate_session
from prof.parsers.field_html_parser import FieldHTMLParser
from prof.work import get_work, all_works
from prof.make import archive_compile
from prof.config import read_config
from prof.tools import check_update
from prof.version import __version__


def print_fields(fields, sort_by_date=False, sort_by_open_projects=False):
    """
    Print a list of available fields and works
    sort_by_date : boolean whether we print works by their due date
    """
    if (not sort_by_date) and (not sort_by_open_projects):
        for (_, name, works) in fields:
            print(name)
            for work in works:
                print('- '+str(work))
    else:
        works = all_works
        # Sort works by due_date
        if sort_by_date:
            works.sort(key=lambda x: (not x.is_open, x.due_date), reverse=True)
        for work in works:
            if sort_by_open_projects:
                if not work.is_open:
                    continue
            print(str(work))


def send_work(fields, baseurl, work_id=None, filename=None, command="make"):
    """Ask user for a file to send to a work"""
    while 1:
        if not work_id:
            try:
                work_id = input("id? ")
            except KeyboardInterrupt:
                exit(0)
        work = get_work(work_id)
        if not work:
            print("id '{0}' not found".format(work_id))
            work_id = None
            continue
        if not work.is_open:  # Verify it is open
            print('"It\'s too late for {0} baby..." (Arnold Schwarzenegger)'.format(work.title))
            work_id = None
            continue
        if not filename:
            try:
                filename = input("filename? ")
            except KeyboardInterrupt:
                exit(0)
        while 1:
            try:
                if command:
                    if not archive_compile(filename, command):
                        print("Compilation failed")
                        try:
                            send = input("Send anyway [y/N] ")
                        except KeyboardInterrupt:
                            exit(0)
                        if send != "y":
                            exit(1)
                            return
                work.upload(baseurl, filename)
                print("Uplodaed, but should verify it on the website")
                return
            except FileNotFoundError:
                print("{0} not found in current dir".format(filename))
                filename = None


def main():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-f', '--filename', help='The name of the file to send to prof')
    argument_parser.add_argument('-i', '--id', help='The project id to upload your file to', type=int)
    argument_parser.add_argument('--sorted', help='Sort project by due dates', action="store_true")
    argument_parser.add_argument('-o', '--display-open-projects', help='Only display open projects', action="store_true")
    argument_parser.add_argument('--login', help='Your prof login', type=str)
    argument_parser.add_argument('--version', help='Print the current version', action="store_true")
    argument_parser.add_argument('--compil-command',
                                 help='The command runned to check project. Defaults to "make"',
                                 type=str,
                                 default="make")
    argument_parser.add_argument('--no-compil',
                                 help='Disable compilation',
                                 action="store_true")
    argument_parser.parse_args()
    arguments = argument_parser.parse_args()

    if arguments.version:
        print("prof {version}".format(version=__version__))
        return

    if check_update():
        print("An update is available. You should ``pip install --upgrade prof``")

    config = read_config()
    baseurl = config['DEFAULT']['baseurl']

    # The actual progression through the website
    prof_session = initiate_session(config)
    fields_html = prof_session.post(baseurl+"/select_projet.php")
    # Parse the project page, and extra available fields
    parser = FieldHTMLParser()
    parser.feed(fields_html.content.decode("iso-8859-1"))
    fields = parser.getFields()

    print_fields(fields, sort_by_date=arguments.sorted, sort_by_open_projects=arguments.display_open_projects)
    compilation_command = "" if arguments.no_compil else arguments.compil_command
    send_work(fields, baseurl, work_id=arguments.id, filename=arguments.filename, command=compilation_command)


if __name__ == "__main__":
    main()
