import os
from os import path
import shutil


loc = "C:\\GitHub"

dist = path.join(loc, "CalciteRTAA\\dist")

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

