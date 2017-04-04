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

environ = "staging"


def system_paths(environ):
    arcmap_path = r"C:\Python27\ArcGIS10.5\python.exe"
    mxd_script = r"C:\GitHub\arcmap\ConvertWebMaptoMXD.py"



    media_dir = {
        "home": "C:/Users/rich/PycharmProjects/rtaa_gis/rtaa_gis/media",
        "work": "C:/GitHub/rtaa_gis/rtaa_gis/media",
        "staging": "C:/inetpub/django_staging/rtaa_gis/rtaa_gis/media",
        "production": "C:/inetpub/django_prod/rtaa_gis/rtaa_gis/media",
    }
    media_dir = media_dir[environ]

    gdb_path = {
        "home": r"G:\GIS Data\Arora\rtaa\MasterGDB_05_25_16\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "work": r"C:\ESRI_WORK_FOLDER\rtaa\MasterGDB\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "staging": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "production": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb"
    }
    gdb_path = gdb_path[environ]

    default_project = {
        "home": r"G:\Documents\ArcGIS\Projects\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "work": r"C:\Users\rhughes\Documents\ArcGIS\Projects\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx"
    }
    default_project = default_project[environ]

    layer_dir = {
        "home": r"G:\GIS Data\Arora\rtaa\layers",
        "work": r"C:\ESRI_WORK_FOLDER\rtaa\layers",
        "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers",
        "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers"
    }
    layer_dir = layer_dir[environ]

    arcpro_path = {
        "work": r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe",
        "home": r"G:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe",
        "staging": r"C:\inetpub\Pro\bin\Python\envs\arcgispro-py3\python.exe",
        "production": r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"
    }
    arcpro_path = arcpro_path[environ]

    mxdx_script = {
        "work": r"C:\GitHub\arcpro\printing\webmap2MXDX.py",
        "home": r"G:\GitHub\arcpro\printing\webmap2MXDX.py",
        "staging": r"C:\GitHub\arcpro\printing\webmap2MXDX.py",
        "production": r"C:\GitHub\arcpro\printing\webmap2MXDX.py"
    }
    mxdx_script = mxdx_script[environ]

    return {
        "arcpro_path": arcpro_path,
        "mxdx_script": mxdx_script,
        "gdb_path": gdb_path,
        "layer_dir": layer_dir,
        "default_project": default_project,
        "media_dir": media_dir
    }


def get_username(request):
    try:
        username = request.META['REMOTE_USER'].split("\\")[-1]
    except KeyError:
        username = request.user.username
    if not len(username):
        username = "Anonymous"
    return username

logger = logging.getLogger(__package__)


# Create your views here.
@api_view(['POST'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_map(request, format=None):
    username = get_username(request)
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
    v = system_paths()
    arcmap_path = v["arcmap_path"]
    mxd_script = v["mxd_script"]

    username = get_username(request)
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


@api_view(['POST', 'GET'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_mxdx(request, format=None):
    v = system_paths(environ)
    arcpro_path = v["arcpro_path"]
    mxdx_script = v["mxdx_script"]
    default_project = v["default_project"]
    gdb_path = v["gdb_path"]
    layer_dir = v["layer_dir"]

    data = request.POST
    if not len(data):
        data = request.query_params

    # write the web map json to a file to bypass command line string limitations
    webmap = data['Web_Map_as_JSON']

    try:
        webmap = json.loads(webmap)

        layout = data['Layout_Template']

        username = get_username(request)
        out_folder = os.path.join(MEDIA_ROOT, username)
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        out_folder = os.path.join(out_folder, 'prints')
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        os.chdir(out_folder)
        temp_file = open('webmap.json', 'w')
        temp_file.write(u"{}".format(json.dumps(webmap)))
        temp_file.close()
    except Exception as e:
        logger.error(e)

    format = data['Format']
    layout_template = data['Layout_Template']

    args = [arcpro_path, mxdx_script, '-username', username, '-media', MEDIA_ROOT,
        '-gdbPath', gdb_path, '-layerDir', layer_dir, '-defaultProject', default_project, '-layout', layout]

    logger.info(args)
    proc = subprocess.Popen(args, stdout=PIPE, stderr=PIPE)

    out = proc.communicate()[0]

    logger.info(out)
    response = Response()
    response['Cache-Control'] = 'no-cache'

    # This format must be identical to the DataFile object returned by the esri print examples
    host = request.META["HTTP_HOST"]

    if host == "127.0.0.1:8080":
        protocol = "http"
    else:
        protocol = "https"

    while proc.returncode is None:
        logger.info("print process return code :: {}".format(proc.returncode))
        proc.wait(1)

    out_file = out.decode().replace("\n", "")
    out_file = out_file.replace("\r", "")

    url = "{}://{}/media/{}/prints/{}".format(protocol, request.META["HTTP_HOST"], username, out_file)

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


@api_view(['POST', 'GET'])
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def getPrintList(request, format=None):
    username = get_username(request)
    print_dir = os.path.join(MEDIA_ROOT, "{}/{}".format(username, "prints"))

    response = Response()
    response.data = list()
    if os.path.exists(print_dir):
        files = os.listdir(print_dir)
        pdfs = [f for f in files if f.endswith(".pdf")]
        response['Cache-Control'] = 'no-cache'

        # This format must be identical to the DataFile object returned by the esri print examples
        host = request.META["HTTP_HOST"]

        if host == "127.0.0.1:8080":
            protocol = "http"
        else:
            protocol = "https"

        for out_file in pdfs:
            url = "{}://{}/media/{}/prints/{}".format(protocol, request.META["HTTP_HOST"], username, out_file)
            response.data.append({"url": url})
    else:
        os.mkdir(print_dir)

    return response


@api_view(['POST'])
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def delete_file(request, format=None):
    username = get_username(request)
    data = request.POST
    file_name = data["filename"].replace("\n", "")
    outfolder = os.path.join(MEDIA_ROOT, "{}/{}".format(username, "prints"))
    if os.path.exists(outfolder):
        os.chdir(outfolder)

        if os.path.exists(file_name):
            os.remove(file_name)
            return Response(data="Temp File {} Deleted from Server".format(file_name))
    else:
        return Response(data="Failed to located user's media folder")
