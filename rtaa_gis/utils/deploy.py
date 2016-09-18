import cgitb
import subprocess
from subprocess import PIPE
cgitb.enable()


def pull(path):
    kwargs = dict()
    kwargs['cwd'] = path
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    git_cmd = "git pull"
    proc = subprocess.Popen(git_cmd, **kwargs)
    (std_out, std_err) = proc.communicate()
    if std_err:
        return std_err
    else:
        return std_out
