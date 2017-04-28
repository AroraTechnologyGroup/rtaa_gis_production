import os
from os import path
import shutil
import sys
import django
import subprocess
from subprocess import PIPE
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rtaa_gis.settings")
django.setup()
from django.conf import settings

BASE_DIR = settings.BASE_DIR
PYTHON_PATH = settings.PYTHON_PATH
loc = r"C:\\GitHub"
dist = path.join(loc, "rtaa_gis_dojo\\dist")

dojo = path.join(dist, "dojo\\dojo.js")
dojo_resources = path.join(dist, "dojo\\resources")
app_images = path.join(dist, "app\\img")
app_resources = path.join(dist, "app\\resources")
app_templates = path.join(dist, "app\\templates")

home = path.dirname(path.dirname(path.abspath(__file__)))
target_folder = path.join(home, "static\\home")

app_folder = path.join(target_folder, "app")
dojo_folder = path.join(target_folder, "dojo")


if path.exists(app_folder):
    shutil.rmtree(app_folder)
    print("{} has been removed".format(app_folder))
if path.exists(dojo_folder):
    shutil.rmtree(dojo_folder)
    print("{} has been removed".format(dojo_folder))

shutil.copytree(dojo_resources, path.join(target_folder, "dojo\\resources"))
shutil.copy2(dojo, os.path.join(target_folder, "dojo\\dojo.js"))
for x in [app_resources, app_images, app_templates]:
    shutil.copytree(x, path.join(target_folder, "app\\{}".format(path.basename(x))))

for dirpath, dirnames, filenames in os.walk(target_folder):
    print(filenames)

kwargs = dict()
kwargs['stderr'] = PIPE
kwargs['stdout'] = PIPE
kwargs['universal_newlines'] = True

manage_script = os.path.join(BASE_DIR, "manage.py")
proc = subprocess.Popen("{} {} collectstatic --no-input".format(PYTHON_PATH, manage_script), **kwargs)
(out, err) = proc.communicate()
if out:
    print(out)
if err:
    print(err)
