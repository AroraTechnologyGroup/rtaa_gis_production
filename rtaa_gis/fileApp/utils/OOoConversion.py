import os
import subprocess
from subprocess import PIPE
from django.http import HttpResponse
open_office_dir = r"C:\Program Files (x86)\OpenOffice 4\program"
open_office_python_path = os.path.join(open_office_dir, "python.exe")
open_office_path = os.path.join(open_office_dir, "soffice")

src_file = os.path.join(open_office_dir, "edoc_conversion.py")
activate_script = os.path.join(open_office_dir, "startOO.py")


class OpenOfficeConverter:
    def __init__(self, in_path):
        self.in_path = in_path
        p = subprocess.Popen([open_office_python_path, activate_script])
        p.wait()

    def convert(self):
        p = subprocess.Popen([open_office_python_path, src_file, self.in_path], stdout=PIPE)
        response = HttpResponse(content_type='application/pdf')
        response.write(p.stdout.read())
        return response
