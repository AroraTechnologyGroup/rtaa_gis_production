import os
import json
import subprocess
import logging
from json.decoder import JSONDecodeError
from subprocess import PIPE
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import list_route, api_view, renderer_classes
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse
from .utils.SearchTool import SearchTool
from .models import GDB, FeatureClass, FeatureDataset, FieldObject, PublisherLog,\
    FeatureLayer, WebMap, DomainValues
from .serializers import FClassSerializer, FDatasetSerializer, GDBSerializer,\
    PLogSerializer, FLayerSerializer, WebMapSerializer, FieldSerializer,\
    BuilderSerializer, DomainSerializer
from django.conf import settings


BASE_DIR = settings.BASE_DIR
arcpy_path = settings.ARCPY_PATH
builder_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils/buildGDBStore.py')

logger = logging.getLogger(__name__)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class Builder(GenericAPIView):
    serializer_class = BuilderSerializer
    queryset = GDB.objects.all()

    def post(self, request, format=None):
        serializer = BuilderSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            gdb = data["gdb"]

            args = [arcpy_path, builder_script, '-gdb', gdb]
            dataset = data["dataset"]
            if dataset:
                args.extend(['-dataset', dataset])
            feature_class = data["featureClass"]
            if feature_class:
                args.extend(['-featureClass', feature_class])
            field = data["field"]
            if field:
                args.extend(['-field', field])

            out_data = []
            proc = subprocess.Popen(args, executable=arcpy_path, stderr=PIPE, stdout=PIPE)
            while proc.poll() is None:
                l = proc.stdout.readline()
                if l:
                    try:
                        out_data.append(json.loads(l.decode('utf8').replace("'", '"')))
                    except JSONDecodeError as e:
                        logger.error(e, l)
                        raise Exception(e, 1)

            # loop through all the json objects and build the store
            for data in out_data:
                if "workspace_type" in data:
                    # this is a geodatabase object
                    # check to see if it exists
                    existing = GDB.objects.filter(catalog_path=data["catalog_path"])
                    if existing:
                        serializer = GDBSerializer(existing[0], data=data)
                    else:
                        serializer = GDBSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.error(serializer.errors)

                elif "code" in data:
                    # this is a domain code and description
                    # get the gdb object to relate these to
                    gdb = GDB.objects.get(base_name=data['gdb_name'])
                    if gdb:
                        data['gdb'] = gdb.pk
                    try:
                        existing = DomainValues.objects.filter(name=data["name"]).get(code=data["code"])
                        serializer = DomainSerializer(existing, data=data)
                    except DomainValues.DoesNotExist:
                        serializer = DomainSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.error(serializer.errors)

                elif "children" in data:
                    # this is a feature dataset object
                    # check to see if it exists
                    existing = FeatureDataset.objects.filter(base_name=data["base_name"])
                    if existing:
                        serializer = FDatasetSerializer(existing[0], data=data)
                    else:
                        serializer = FDatasetSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.error(serializer.errors)

                elif "field_list" in data:
                    # this is a feature class object
                    # check to see if it exists
                    existing = FeatureClass.objects.filter(catalog_path=data["catalog_path"])
                    if existing:
                        serializer = FClassSerializer(existing[0], data=data)
                    else:
                        serializer = FClassSerializer(data=data)

                    if serializer.is_valid():
                        serializer.save()
                    else:
                        logger.error(serializer.errors)

                elif "percent" in data:
                    # this is a Field Object
                    # check to see if the field object exists
                    existing = FieldObject.objects.filter(name=data["name"])
                    if existing:
                        serializer = FieldSerializer(existing[0], data=data)
                    else:
                        serializer = FieldSerializer(data=data)

                    if serializer.is_valid():
                        field = serializer.save()
                        domain_rows = DomainValues.objects.filter(name=data["domain_name"])
                        if domain_rows:
                            for x in domain_rows:
                                x.fieldobject_set.add(field)
                    else:
                        logger.error(serializer.errors)

            return Response(data=out_data)

        else:

            return Response(data=serializer.errors)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GDBSummaryPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'GDB_Summary.html'

    @list_route(methods=['get',])
    def get(self, request, format=None):
        gdb = GDB.objects.all()
        dsets = FeatureDataset.objects.all()
        fcs = FeatureClass.objects.all()
        fields = FieldObject.objects.all()

        data = {'gdb': gdb, 'dsets': dsets, 'fcs': fcs, 'fields': fields}
        return Response(data=data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class OnlineViewSet(viewsets.ViewSet):
    renderer_classes = (JSONRenderer,)

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
class WebMapViewSet(viewsets.ModelViewSet):
    queryset = WebMap.objects.all()
    serializer_class = WebMapSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FLayerViewSet(viewsets.ModelViewSet):
    queryset = FeatureLayer.objects.all()
    serializer_class = FLayerSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GDBViewSet(viewsets.ModelViewSet):
    queryset = GDB.objects.all()
    serializer_class = GDBSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FDatasetViewSet(viewsets.ModelViewSet):
    queryset = FeatureDataset.objects.all()
    serializer_class = FDatasetSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FClassViewSet(viewsets.ModelViewSet):
    queryset = FeatureClass.objects.all()
    serializer_class = FClassSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class FieldViewSet(viewsets.ModelViewSet):
    queryset = FieldObject.objects.all()
    serializer_class = FieldSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class PLogViewSet(viewsets.ModelViewSet):
    queryset = PublisherLog.objects.all()
    serializer_class = PLogSerializer




