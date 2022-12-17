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
    if command == "":
        return True
    with tempfile.TemporaryDirectory(suffix="prof") as tmpdir:
        with tarfile.open(filename) as tararchive:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tararchive, tmpdir)
            cwd = os.getcwd()  # get current directory
            try:
                os.chdir(tmpdir)
                print("Running {} in {} for file {}".format(command, tmpdir, filename))
                make = os.system(command)
                if make == 0:
                    print("Successfully compiled")
                    return True
            finally:
                os.chdir(cwd)
    return False
