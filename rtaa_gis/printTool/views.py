from rest_framework.decorators import api_view
import logging
from rest_framework.response import Response
import arcgis
from arcgis import mapping

logger = logging.getLogger(__package__)

gis = arcgis.gis.GIS(url="https://rtaa.maps.arcgis.com",
                     username="data_owner",
                     password="GIS@RTAA123!")


# Create your views here.
@api_view(['GET', 'POST'])
def print_map(request, format=None):
    data = request.POST
    webmap = data['Web_Map_as_JSON']
    format = data['Format']
    layout_template = data['Layout_Template']
    data = mapping.export_map(web_map_as_json=webmap, format=format,
                       layout_template=layout_template,
                       gis=gis)
    resp = Response()
    resp.data = data.url
    return resp
