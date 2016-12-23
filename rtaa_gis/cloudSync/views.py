import os
import json
import subprocess
from subprocess import PIPE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import list_route
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from .utils.SearchTool import SearchTool
from .models import GDB, FeatureClass, FeatureDataset, PublisherLog
from .serializers import FClassSerializer, FDatasetSerializer, GDBSerializer, PLogSerializer
from rtaa_gis.settings import BASE_DIR

arcpro_path = r"C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe"

gdb_build_script = r"C:\GitHub\arcpro\buildGDBStore.py"


@method_decorator(ensure_csrf_cookie, name='dispatch')
class OnlineViewSet(viewsets.ViewSet):
    renderer_classes = (JSONRenderer,)
    queryset = PublisherLog.objects.all()

    @list_route(methods=['get', 'post'])
    def feature_layers(self, request):
        x = SearchTool("Feature Layer")
        items = x.search_all()
        final_list = []
        for x in items:
            new_item = {
                "id": x["id"],
                "title": x["title"],
                "spatialReference": x["spatialReference"],
                "url": x["url"]
            }
            final_list.append(new_item)
        return Response(final_list)

    @list_route(methods=['get', 'post'])
    def web_maps(self, request):
        x = SearchTool("Web Map")
        items = x.search_all()
        final_list = []
        for x in items:
            new_item = {
                "id": x["id"]
            }
            final_list.append(new_item)
        return Response(final_list)

    @list_route(methods=['get', 'post'])
    def web_apps(self, request):
        x = SearchTool("Web App")
        items = x.search_all()
        final_list = []
        for x in items:
            new_item = {
                "id": x["id"]
            }
            final_list.append(new_item)
        return Response(final_list)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FClassViewSet(viewsets.ModelViewSet):
    queryset = FeatureClass.objects.all()
    serializer_class = FClassSerializer

    # @list_route(methods=['get', 'post'])
    def get(self, request, format=None):
        serializer = FClassSerializer(self.queryset.data, many=True, context={'request': request})
        return Response(serializer.data)

    @list_route(methods=['get', 'post'])
    def _build(self, request):
        build_script = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    gdb_build_script)
        proc = subprocess.Popen(["{}".format(arcpro_path), build_script], stdout=PIPE)
        out, err = proc.communicate()
        if out:
            conv = out.decode()
            conv2 = conv.replace("'", '"')
            item = json.loads(conv2)

            kwargs = {
                "baseName": item["baseName"],
                "workspaceType": item["workspaceType"],
                "catalogPath": item["catalogPath"],
                "workspaceFactoryProgID": item["workspaceFactoryProgID"],
                "release": item["release"],
                "domains": item["domains"],
                "currentRelease": item["currentRelease"],
                "connectionString": item["connectionString"]
            }

            try:
                existing_gdb = GDB.objects.get(catalogPath=kwargs["catalogPath"])
                existing_gdb.update(**kwargs)
                existing_gdb.save()
            except GDB.DoesNotExist:
                GDB.objects.create(**kwargs)

            datasets = item["datasets"]
            for dset in datasets:
                kwargs = {
                    "baseName": dset["baseName"],
                    "changeTracked": dset["changeTracked"],
                    "datasetType": dset["datasetType"],
                    "isVersioned": dset["isVersioned"],
                    "spatialReference": dset["spatialReference.name"],
                    "children": dset["children"]
                }
                FeatureDataset.objects.create(**kwargs)

                for fc in dset["feature_classes"]:
                    kwargs = {
                        "catalogPath": fc["catalogPath"],
                        "baseName": fc["baseName"],
                        "count": fc["count"],
                        "featureType": fc["featureType"],
                        "hasM": fc["hasM"],
                        "hasZ": fc["hasZ"],
                        "hasSpatialIndex": fc['hasSpatialIndex'],
                        "shapeFieldName": fc["shapeFieldName"],
                        "shapeType": fc["shapeType"]
                    }
                    FeatureClass.objects.create(**kwargs)

            return Response(conv2)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class PLogViewSet(viewsets.ModelViewSet):
    queryset = PublisherLog.objects.all()
    serializer_class = PLogSerializer

    def get(self, request, format=None):
        serializer = PLogSerializer(self.queryset.data, many=True, context={'request': request})
        return Response(serializer.data)



