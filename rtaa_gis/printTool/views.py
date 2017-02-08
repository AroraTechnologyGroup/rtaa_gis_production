from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework_jsonp.renderers import JSONPRenderer
import logging
import os
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

logger = logging.getLogger(__package__)

# Create your views here.
@api_view(['POST'])
# @renderer_classes((JSONPRenderer,))
@authentication_classes((AllowAny,))
@ensure_csrf_cookie
def print_map(request, format=None):
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
    webmap = json.dumps(map_obj)

    format = data['Format']
    layout_template = data['Layout_Template']
    data = mapping.export_map(web_map_as_json=webmap, format=format,
                       layout_template=layout_template,
                       gis=gis)
    file = data.download(MEDIA_ROOT)
    file_name = os.path.basename(file)

    os.chdir(MEDIA_ROOT)
    mime_type = mimetypes.guess_type(file)
    extension = file.split(".")[-1]
    base_name = "GISViewer_export"
    full_name = "{}.{}".format(base_name, extension)
    if os.path.exists(full_name):
        full_name = "{}_1.{}".format(base_name, extension)
        if os.path.exists(full_name):
            i = False
            while not i:
                splits = full_name.split("_")
                full_name = "{}_{}.{}".format(base_name, int(splits[-1].split('.')[0]) + 1, extension)
                if not os.path.exists(full_name):
                    i = True


    try:
        os.rename(file_name, full_name)
    except OSError:
        logging.error("printed map unable to be saved")

    response = Response()
    # This format must be identical to the DataFile object returned by the esri print examples
    response.data = {
        "messages": [],
        "results": [{
            "value": {
                "url": "https://gisapps.aroraengineers.com:8004/media/{}".format(full_name)
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
    return Response(data="File Deleted from Server")
