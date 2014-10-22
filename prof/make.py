import os
import tarfile
import tempfile


def archive_compile(filename, command="make"):
    """
    Returns if the given archive properly compile.
    Extract it in a temporary directory, run the given command, and return True it's result is 0
    """
    if not tarfile.is_tarfile(filename):
        print("Cannot extract archive")
        return False
    with tempfile.TemporaryDirectory(suffix="prof") as tmpdir:
        with tarfile.open(filename) as tararchive:
            tararchive.extractall(tmpdir)
            cwd = os.getcwd()  # get current directory
            try:
                os.chdir(tmpdir)
                print("Running {} in {} for file {}".format(command, tmpdir, filename))
                make = os.system("make")
                if make == 0:
                    print("Successfully compiled")
                    return True
            finally:
                os.chdir(cwd)
    return False
