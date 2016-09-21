from rtaa_gis.settings import BASE_DIR
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

    kwargs = dict()
    kwargs['cwd'] = BASE_DIR
    kwargs['stderr'] = PIPE
    kwargs['stdout'] = PIPE
    kwargs['universal_newlines'] = True
    python_path = r"venv\scripts\python.exe"
    manage_script = "manage.py"
    proc = subprocess.Popen("{} {} collectstatic --no-input".format(python_path, manage_script), **kwargs)
    (out, err) = proc.communicate()

    connection = mail.get_connection()
    connection.open()
    send_mail(
        "Deploy RTAA_GIS to Staging",
        "std_out: {}\n std_err: {}\n collectstatic: {}\n err: {}".format(std_out, std_err, out, err),
        "rhughes@aroraengineers.com",
        ["richardh522@gmail.com"],
        fail_silently=False,
    )
    connection.close()
    if std_err:
        return std_err
    else:
        return std_out
