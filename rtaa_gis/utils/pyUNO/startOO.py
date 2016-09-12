import subprocess
import os
this_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_dir)
p = subprocess.Popen(['soffice', '-headless', '-nofirststartwizard',
                      '-accept=pipe,name=abraxas;urp;StarOffice.Servicemanager'])
