import cgitb
import subprocess
from subprocess import PIPE
from django.core.mail import send_mail
from django.core import mail
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

    connection = mail.get_connection()
    connection.open()
    send_mail(
        "Deploy RTAA_GIS to Staging",
        "std_out: {} \n std_err: {}".format(std_out, std_err),
        "rhughes@aroraengineers.com",
        ["richardh522@gmail.com"],
        fail_silently=False,
    )
    connection.close()
    if std_err:
        return std_err
    else:
        return std_out
