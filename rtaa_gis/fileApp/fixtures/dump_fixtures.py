import os
import subprocess
from subprocess import PIPE

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def dump(model):
    kwargs = dict()
    kwargs['cwd'] = BASE_DIR
    kwargs['stdout'] = PIPE
    kwargs['stderr'] = PIPE
    proc = subprocess.Popen("python manage.py dumpdata fileApp.{0} --indent 4 --output fileApp/fixtures/json/{1}.json".format(model, model.lower()),
                            **kwargs)
    std_out, std_err = proc.communicate()
    if std_out:
        print(std_out)
    if std_err:
        print(std_err)

models = ['FileModel', 'GridCell', 'Assignment']
for x in models:
    dump(x)
