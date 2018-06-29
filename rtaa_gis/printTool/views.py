from __future__ import unicode_literals
from analytics.serializers import RecordSerializer
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from django.http import JsonResponse
from django.contrib.auth.models import User
import logging
import os
import sys
import requests
import subprocess
from subprocess import PIPE
from subprocess import TimeoutExpired
import arcgis
from arcgis import mapping
from PIL import Image
from io import BytesIO

from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from io import BytesIO
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.files import File
from django.core import mail
from datetime import datetime, date
import mimetypes
import json
import shlex
import threading
import traceback
import time
from datetime import datetime
from django.conf import settings
MEDIA_ROOT = settings.MEDIA_ROOT
STATIC_ROOT = settings.STATIC_ROOT
LDAP_URL = settings.LDAP_URL
DEBUG = settings.DEBUG

logger = logging.getLogger(__name__)


def loggit(text):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    logger.error(traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2))


def system_paths(environ):
    arcmap_path = {
        "work": r"C:\Python27\ArcGIS10.4\python.exe",
        "rtaa_testing": r"C:\Python27\ArcGIS10.5\python.exe"
    }
    arcmap_path = arcmap_path[environ]

    mxd_script = {
        "work": r"C:\GitHub\rtaa_gis\rtaa_gis\printTool\utils\ConvertWebMaptoMXD.py",
        "rtaa_testing": r"C:\GitHub\rtaa_gis_django\rtaa_gis\printTool\utils\ConvertWebMaptoMXD.py"
    }
    mxd_script = mxd_script[environ]

    media_dir = {
        "work": "C:/GitHub/rtaa_gis/rtaa_gis/media",
        "staging": r"C:/GitHub/rtaa_gis_django/rtaa_gis/rtaa_gis/media",
        "production": "C:/inetpub/django_prod/rtaa_gis/rtaa_gis/media",
        "rtaa_testing": r"C:\inetpub\rtaa_gis_django_testing\rtaa_gis\media"
    }
    media_dir = media_dir[environ]

    gdb_path = {
        "work": r"C:\ESRI_WORK_FOLDER\rtaa\MasterGDB\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "staging": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "production": r"C:\inetpub\rtaa_gis_data\MasterGDB_05_25_16\MasterGDB_05_25_16.gdb",
        "rtaa_testing": r"D:\ConnectionFiles\OSAuth@RTAA_MasterGDB.sde"
    }
    gdb_path = gdb_path[environ]

    default_project = {
        "work": r"C:\Users\rhughes\Documents\ArcGIS\Projects\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\RTAA_Printing_Publishing.aprx",
        "rtaa_testing": r"D:\ArcPro\RTAA_Publishing\RTAA_Publishing.aprx"
    }
    default_project = default_project[environ]

    layer_dir = {
        "work": r"C:\ESRI_WORK_FOLDER\rtaa\layers",
        "staging": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers",
        "production": r"C:\inetpub\rtaa_gis_data\RTAA_Printing_Publishing\FeatureLayers",
        "rtaa_testing": r"D:\ArcPro\RTAA_Publishing\FeatureLayers"
    }
    layer_dir = layer_dir[environ]

    return {
        "arcmap_path": arcmap_path,
        "mxd_script": mxd_script,
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
        # This value is used for testing AJAX requests to the dev runserver
        username = "siteadmin"
    return username


def apply_watermark(watermark, target):
    try:
        logger.info(os.path.abspath(__file__))
        wmark_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), r'media\printTool\{}'.format(watermark))
        wmark = PdfFileReader(open(wmark_file, "rb"))
        output_file = PdfFileWriter()
        input_file = PdfFileReader(open(target, "rb"))
        combo_name = os.path.join(os.path.dirname(target), "{}_temp.pdf".format(os.path.basename(target).replace(".pdf", "")))
        new_file = canvas.Canvas(combo_name)
        new_file.save()

        page_count = input_file.getNumPages()

        for page_number in range(page_count):
            print("Watermarking page {} of {}".format(page_number, page_count))
            input_page = input_file.getPage(page_number)
            input_page.mergePage(wmark.getPage(0))
            output_file.addPage(input_page)

        with open(combo_name, "wb") as outputStream:
            output_file.write(outputStream)

        # closing the streams allows the files to be renamed/removed
        wmark.stream.close()
        input_file.stream.close()

        os.remove(target)
        os.rename(combo_name, target)
        return target

    except Exception as e:
        loggit(e)


def name_file(out_folder, new_name, extension):
    full_name = "{}.{}".format(new_name, extension)

    if os.path.exists(os.path.join(out_folder, full_name)):
        v = 1
        full_name = "{}_{}.{}".format(new_name, v, extension)
        if os.path.exists(os.path.join(out_folder, full_name)):
            i = False
            while not i:
                v += 1
                full_name = "{}_{}.{}".format(new_name, v, extension)
                if not os.path.exists(os.path.join(out_folder, full_name)):
                    i = True

    return os.path.join(out_folder, full_name)


# Create your views here.
@api_view(['POST'])
@ensure_csrf_cookie
def layout(request, format=None):
    try:
        username = get_username(request)
        # the user's folder is created when they access the home page
        out_folder = os.path.join(MEDIA_ROOT, r'users\{}\prints'.format(username))
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        data = request.POST
        url = data["url"]
        title = data["title"]
        layout_template = data['layout_template']

        # set the filename to be the Title of the map
        filename = name_file(out_folder, title, "pdf")

        # download the pdf map print from AGOL
        file = requests.get(url, auth=('data_owner', 'GIS@RTAA123!'))

        pdfOutputFile = open(filename, 'wb')
        pdfOutputFile.write(file.content)
        pdfOutputFile.close()

        # apply the watermark

        watermark = None
        if layout_template == "Letter ANSI A Landscape":
            watermark = "Watermark_8_5_11_landscape.pdf"
        elif layout_template == "Letter ANSI A Portrait":
            watermark = "Watermark_8_5_11_portrait.pdf"
        elif layout_template == "Tabloid ANSI B Landscape":
            watermark = "Watermark_11_17_landscape.pdf"
        elif layout_template == "Tabloid ANSI B Portrait":
            watermark = "Watermark_11_17_portrait.pdf"

        apply_watermark(watermark=watermark, target=filename)

        # rename map print and graphics file if it exists at temp.json
        graphics_file = os.path.join(out_folder, 'temp.json')
        if os.path.exists(graphics_file):
            new_name = name_file(out_folder, title, "json")
            os.rename(graphics_file, new_name)

        host = request.META["HTTP_HOST"]
        media_url = settings.MEDIA_URL.lstrip("/")
        media_url = media_url.rstrip("/")

        if host == "127.0.0.1:8080":
            protocol = "http"
        else:
            protocol = "https"

        url = "{}://{}/{}/users/{}/prints/{}".format(protocol, host, media_url, username, os.path.basename(filename))

        data = {
            "method": "print",
            "app_name": "Print"
        }
        serial = RecordSerializer(data=data, context={'request': request})
        if serial.is_valid():
            serial.save()
        else:
            logger.error("Unable to save count :: {}".format(data))
        return JsonResponse({"url": url})
    except Exception as e:
        loggit(e)


@api_view(['POST'])
@ensure_csrf_cookie
def parseGraphics(request, format=None):
    try:
        username = get_username(request)
        out_folder = os.path.join(MEDIA_ROOT, 'users/{}/prints'.format(username))
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)

        web_map = request.data.get('web_map_json')
        map = json.loads(web_map)
        op_layers = map["operationalLayers"]

        # create an initial temp graphics file to rename
        tempfile = os.path.join(out_folder, "temp.json")
        temp_file = open(tempfile, 'w')

        cont = []
        for x in op_layers:
            if "draw_results" in x["id"].lower() or "map_graphics" in x["id"].lower():
                cont.append(x)
        json_cont = json.dumps(cont).replace("False", "false").replace("True", "true").replace("None", "null")
        temp_file.write(json_cont)
        temp_file.close()

        resp = Response()
        # read json file, if it is empty delete it from the server
        text = open(tempfile, 'r').read()
        if text == "[]":
            os.remove(tempfile)
            resp.data = {"message": "Empty drawings graphics"}
        else:
            resp.data = {"message": "Graphics file saved"}
        return resp

    except Exception as e:
        loggit(e)


@api_view(['GET'])
@ensure_csrf_cookie
def agol_user(request, format=None):
    try:
        ldap_username = get_username(request)
        user_obj = User.objects.get(username=ldap_username)
        email = user_obj.email
        firstName = user_obj.first_name
        lastName = user_obj.last_name

        if ldap_username == "siteadmin":
            firstName = "siteadmin"
            lastName = "siteadmin"

        # get the user info from our database
        user_obj = User.objects.get(username=username)
        firstName = user_obj.first_name
        lastName = user_obj.last_name
        email = user_obj.email

        if LDAP_URL == "gis.renoairport.net":
            provider = "enterprise"
            password = None
            username = "{}_RTAA".format(email)
            idpUsername = ldap_username

        else:
            provider = "arcgis"
            password = "testeruser123"
            username = "{}".format(ldap_username)
            idpUsername = None

        gis = arcgis.gis.GIS(url="https://rtaa.maps.arcgis.com",
                             username="data_owner",
                             password="GIS@RTAA123!")
        me = gis.users.me
        account = gis.users.get(username="{}".format(username))

        resp = Response()
        if account:
            pass
            # account.delete(reassign_to='data_owner')
            resp.data = {"code": 0, "message": ldap_username}
        else:
            user = gis.users.create(username=username,
                                    password=password,
                                    firstname=firstName,
                                    lastname=lastName,
                                    email=email,
                                    level=1,
                                    role="org_viewer",
                                    provider=provider)
            if user:
                resp.data = {"code": 0,
                             "message": username}
            else:
                resp.data = {"code": -1,
                             "message": "error. Unable to create user"}

        return resp

    except Exception as e:
        loggit(e)


@api_view(['GET'])
# @authentication_classes((AllowAny,))
@ensure_csrf_cookie
def getPrintList(request, format=None):
    username = get_username(request)
    print_dir = os.path.join(MEDIA_ROOT, "users/{}/prints".format(username))
    logger.info(print_dir)

    response = Response()
    response.data = list()
    if os.path.exists(print_dir):
        files = os.listdir(print_dir)
        # selection will hold the files with the specified extensions
        selection = []
        for x in [".png", ".pdf", ".jpg", ".gif", ".eps", ".svg", ".svgz"]:
            selection.extend([f for f in files if f.endswith(x)])

        response['Cache-Control'] = 'no-cache'
        host = request.META["HTTP_HOST"]
        if host == "127.0.0.1:8080":
            protocol = "http"
        else:
            protocol = "https"
        media_url = settings.MEDIA_URL.lstrip("/")
        media_url = media_url.rstrip("/")

        for out_file in selection:
            url = "{}://{}/{}/users/{}/prints/{}".format(protocol, host, media_url, username, out_file)
            sec = os.path.getmtime(os.path.join(print_dir, out_file))
            date = datetime.fromtimestamp(sec).date().isoformat()
            response.data.append({"date": date, "url": url})
    else:
        response.data.append("Error, print directory not found")

    return response


@api_view(['GET'])
# @authentication_classes((AllowAny,))
@ensure_csrf_cookie
def getMarkupList(request, format=None):
    username = get_username(request)
    print_dir = os.path.join(MEDIA_ROOT, "users/{}/prints".format(username))
    logger.info(print_dir)
    response = Response()
    response.data = list()
    if os.path.exists(print_dir):
        files = os.listdir(print_dir)
        selection = [x for x in files if x.endswith(".json")]
        response['Cache-Control'] = 'no-cache'
        host = request.META["HTTP_HOST"]
        if host == "127.0.0.1:8080":
            protocol = "http"
        else:
            protocol = "https"
        media_url = settings.MEDIA_URL.lstrip("/")
        media_url = media_url.rstrip("/")
        for out_file in selection:
            full_path = os.path.join(print_dir, out_file)
            # count the number of graphics
            obj = json.loads(open(full_path).read())
            feature_cnt = 0
            layers = obj[0]["featureCollection"]["layers"]
            for x in layers:
                feats = x["featureSet"]["features"]
                feature_cnt += len(feats)

            sec = os.path.getmtime(full_path)
            date = datetime.fromtimestamp(sec).date().isoformat()
            url = "{}://{}/{}/users/{}/prints/{}".format(protocol, host, media_url, username, out_file)
            response.data.append({"date": date, "url": url, "feature_count": feature_cnt})
    else:
        response.data.append("Error, print directory not found")

    return response


@api_view(['POST'])
# @authentication_classes((AllowAny,))
@ensure_csrf_cookie
def delete_file(request, format=None):
    username = get_username(request)
    data = request.POST
    file_name = data["filename"].replace("\n", "")
    outfolder = os.path.join(MEDIA_ROOT, r"users\{}\prints".format(username))
    response = Response()

    if os.path.exists(outfolder):
        old_dir = os.getcwd()
        os.chdir(outfolder)
        if os.path.exists(file_name):
            os.remove(file_name)
            data = "File {} Deleted from Server".format(file_name)
        else:
            data = "File {} not found in user's print folder".format(file_name)
        os.chdir(old_dir)
    else:
        data = "Failed to located user's media folder"
    response.data = data
    return response


@api_view(['POST'])
# @authentication_classes((AllowAny,))
@ensure_csrf_cookie
def emailExhibit(request, format=None):
    username = get_username(request)
    data = request.POST
    exhibit_url = data["exhibit_url"].replace("\n", "")
    recipient = data["recipient"].replace("\n", "")

    cc = data["cc"]
    if type(cc) is str:
        cc = [cc]

    bcc = ["rhughes@aroraengineers.com"]
    from_email = "{}@renoairport.net".format(username)
    # to allow for testing
    if settings.LDAP_URL == "gisapps.aroraengineers.com":
        recipient = "richardh522@gmail.com"
        from_email = "rhughes@aroraengineers.com"
        cc = ["rhughes@aroraengineers.com"]
    subject = data["subject"].replace("\n", "")
    message = data["message"].replace("\n", "")
    splits = exhibit_url.split("/")
    start = splits.index("users")
    server_file = os.path.join(MEDIA_ROOT, "/".join(splits[start:]))
    base_name = os.path.basename(server_file)
    content = open(server_file, 'rb').read()

    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject="{}".format(subject),
            body="From - {} \n {}".format(username, message),
            from_email=from_email,
            to=[recipient],
            cc=cc,
            bcc=bcc,
            attachments=[(base_name, content, 'application/pdf')],
            connection=connection
        ).send()

    response = Response("success")
    return response