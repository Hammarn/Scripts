import argparse
import subprocess
import pandas as pd


def execute_command_line(cl, shell=False, stdout=None, stderr=None, cwd=None):
    """Execute a command line and return the subprocess.Popen object.
    :param cl: Can be either a list or a string; if string, gets shlex.splitted
    :param bool shell: value of shell to pass to subprocess
    :param file stdout: The filehandle destination for STDOUT (can be None)
    :param file stderr: The filehandle destination for STDERR (can be None)
    :param str cwd: The directory to be used as CWD for the process launched
    :returns: The subprocess.Popen object
    :rtype: subprocess.Popen
    :raises RuntimeError: If the OS command-line execution failed.
    """
    if cwd and not os.path.isdir(cwd):
        LOG.warning("CWD specified, \"{}\", is not a valid directory for "
                 "command \"{}\". Setting to None.".format(cwd, cl))
        ## FIXME Better to just raise an exception
        cwd = None
    if type(cl) is str and shell == False:
        LOG.info("Executing command line: {}".format(cl))
        cl = shlex.split(cl)
    if type(cl) is list and shell == True:
        cl = " ".join(cl)
        LOG.info("Executing command line: {}".format(cl))
    try:
        p_handle = subprocess.Popen(cl, stdout=stdout,
                                        stderr=stderr,
                                        cwd=cwd,
                                        shell=shell)
        error_msg = None
    except OSError:
        error_msg = ("Cannot execute command; missing executable on the path? "
                     "(Command \"{}\")".format(cl))
    except ValueError:
        error_msg = ("Cannot execute command; command malformed. "
                     "(Command \"{}\")".format(cl))
    except subprocess.CalledProcessError as e:
        error_msg = ("Error when executing command: \"{}\" "
                     "(Command \"{}\")".format(e, cl))
    if error_msg:
        raise RuntimeError(error_msg)
return p_handle






if __name__ == "__main__":
    # Command line arguments
    parser = argparse.ArgumentParser("Merge two plink datasets together")
    parser.add_argument("-1", "--one", required=True)
help="Input file one")
    parser.add_argument("-2", "--two", required=True)
help="Input file two")
    parser.add_argument("-o", "--out", required=True)
help="Name of output")



args = parser.parse_args()
