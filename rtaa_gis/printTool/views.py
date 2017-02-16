from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework_jsonp.renderers import JSONPRenderer
import logging
import os
import sys
import subprocess
from subprocess import PIPE
from subprocess import TimeoutExpired
import arcgis
from arcgis import mapping
from rtaa_gis.settings import MEDIA_ROOT
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from io import BytesIO
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files import File
from datetime import datetime
import mimetypes
import json
import shlex

arcmap_path = r"C:\Python27\ArcGIS10.5\python.exe"
mxd_script = r"C:\GitHub\arcmap\ConvertWebMaptoMXD.py"

#work laptop
# arcpro_path = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"
arcpro_path = r"C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\propy"
if not os.path.exists(arcpro_path):
    # home pc
    arcpro_path = r"G:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

# work laptop
mxdx_script = r"C:\GitHub\arcpro\printing\webmap2MXDX.py"
if not os.path.exists(mxdx_script):
    # home pc
    mxdx_script = r"G:\GitHub\arcpro\printing\webmap2MXDX.py"

# azure staging
gdbPath = r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb"
if not os.path.exists(gdbPath):
    # work laptop
    gdbPath = r"C:\ESRI_WORK_FOLDER\rtaa\MasterGDB\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb"
if not os.path.exists(gdbPath):
    # home pc
    gdbPath = r"G:\GIS Data\Arora\rtaa\MasterGDB_05_25_16\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb"

# azure staging
layerDir = r"C:\inetpub\rtaa_gis_data\layers"
if not os.path.exists(layerDir):
    # work laptop
    layerDir = r"C:\ESRI_WORK_FOLDER\rtaa\layers"
if not os.path.exists(layerDir):
    # home Pc
    layerDir = r"G:\GIS Data\Arora\rtaa\layers"

#azure staging
defaultProject = r"C:\inetpub\rtaa_gis_data\RTAA_Printing.aprx"
if not os.path.exists(defaultProject):
    # work laptop
    defaultProject = r"C:\Users\rhughes\Documents\ArcGIS\Projects\RTAA_Printing\RTAA_Printing.aprx"
if not os.path.exists(defaultProject):
    # home pc
    defaultProject = r"G:\Documents\ArcGIS\Projects\RTAA_Printing\RTAA_Printing.aprx"

logger = logging.getLogger(__package__)


# Create your views here.
@api_view(['POST'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_map(request, format=None):
    username = request.user.username
    if not len(username):
        username = "Anonymous"
    out_folder = os.path.join(MEDIA_ROOT, username)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)

    gis = arcgis.gis.GIS(url="https://rtaa.maps.arcgis.com",
                         username="data_owner",
                         password="GIS@RTAA123!")

    token = gis._con._token
    logger.info(token)
    data = request.POST

    webmap = data['Web_Map_as_JSON']
    map_obj = json.loads(webmap)
    for x in map_obj["operationalLayers"]:
        if "token" in x.keys():
            print(x["token"])
            x["token"] = token
            print(x["token"])

    format = data['Format']
    layout_template = data['Layout_Template']
    data = mapping.export_map(web_map_as_json=webmap, format=format,
                       layout_template=layout_template,
                       gis=gis)

    file = data.download(out_folder)
    file_name = os.path.basename(file)

    os.chdir(out_folder)
    mime_type = mimetypes.guess_type(file)
    extension = file.split(".")[-1]
    base_name = "GISViewer_export"
    full_name = "{}.{}".format(base_name, extension)
    if os.path.exists(full_name):
        v = 1
        full_name = "{}_{}.{}".format(base_name, v, extension)
        if os.path.exists(full_name):
            i = False
            while not i:
                v += 1
                full_name = "{}_{}.{}".format(base_name, v, extension)
                if not os.path.exists(full_name):
                    i = True


    try:
        os.rename(file_name, full_name)
    except OSError:
        logging.error("printed map unable to be saved with correct filename")

    response = Response()
    # This format must be identical to the DataFile object returned by the esri print examples
    host = request.META["HTTP_HOST"]

    if host == "127.0.0.1:8080":
        protocol = "http"
    else:
        protocol = "https"

    url = "{}://{}/{}/{}".format(protocol, request.META["HTTP_HOST"], out_folder, full_name)

    response.data = {
        "messages": [],
        "results": [{
            "value": {
                "url": url
            },
            "paramName": "Output_File",
            "dataType": "GPDataFile"
        }]
    }
    return response


@api_view(['POST'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_mxd(request, format=None):
    username = request.user.username
    if not len(username):
        username = "Anonymous"
    data = request.POST
    webmap = data['Web_Map_as_JSON']
    out_folder = os.path.join(MEDIA_ROOT, username)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    os.chdir(out_folder)

    temp_file = open('webmap.json', 'w')
    temp_file.write(webmap)
    temp_file.close()

    format = data['Format']
    layout_template = data['Layout_Template']

    args = [arcmap_path, mxd_script, '-username', username, '-media', MEDIA_ROOT, '-layout', layout_template, '-format', format]
    proc = subprocess.Popen(args, executable=arcmap_path, stderr=PIPE, stdout=PIPE)
    out, err = proc.communicate()

    response = Response()
    # This format must be identical to the DataFile object returned by the esri print examples
    host = request.META["HTTP_HOST"]

    if host == "127.0.0.1:8080":
        protocol = "http"
    else:
        protocol = "https"

    url = "{}://{}/media/{}/{}".format(protocol, request.META["HTTP_HOST"], username, "layout.pdf")

    response.data = {
        "messages": [],
        "results": [{
            "value": {
                "url": url
            },
            "paramName": "Output_File",
            "dataType": "GPDataFile"
        }]
    }
    return response


@api_view(['POST'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_mxdx(request, format=None):
    try:
        username = request.META['REMOTE_USER'].split("\\")[-1]
    except KeyError:
        username = request.user.username
    if not len(username):
        username = "Anonymous"

    logger.info(username)
    data = request.POST
    # write the web map json to a file to bypass command line string limitations
    webmap = data['Web_Map_as_JSON']
    out_folder = os.path.join(MEDIA_ROOT, username)
    if not os.path.exists(out_folder):
        os.mkdir(out_folder)
    os.chdir(out_folder)

    temp_file = open('webmap.json', 'w')
    temp_file.write(webmap)
    temp_file.close()

    format = data['Format']
    layout_template = data['Layout_Template']

    args = [arcpro_path, mxdx_script, '-username', username, '-media', MEDIA_ROOT,
            '-gdbPath', gdbPath, '-layerDir', layerDir, '-defaultProject', defaultProject]
    logger.info(args)
    proc = subprocess.Popen(args, stdout=PIPE)

    out = proc.communicate()[0]
    logger.info("return value from subprocess print script :: {}".format(str(out)))
    response = Response()
    response['Cache-Control'] = 'no-cache'

    # This format must be identical to the DataFile object returned by the esri print examples
    host = request.META["HTTP_HOST"]

    if host == "127.0.0.1:8080":
        protocol = "http"
    else:
        protocol = "https"

    while proc.returncode is None:
        proc.wait(1)

    url = "{}://{}/media/{}/{}".format(protocol, request.META["HTTP_HOST"], username, "layout.pdf")

    response.data = {
        "messages": [],
        "results": [{
            "value": {
                "url": url
            },
            "paramName": "Output_File",
            "dataType": "GPDataFile"
        }]
    }

    return response


@api_view(['POST'])
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def delete_file(request, format=None):
    data = request.POST
    file_name = data["filename"]
    os.chdir(MEDIA_ROOT)
    if os.path.exists(file_name):
        os.remove(file_name)
    return Response(data="Temp File {} Deleted from Server".format(file_name))
