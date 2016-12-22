import os
from subprocess import PIPE
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils.SearchTool import SearchTool
import json


# Create your views here
class ViewLayers(APIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template = r'cloudSync\OnlineLayers.html'

    def get(self, request, *args, **kwargs):
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
        resp = Response(template_name=self.template, data={"layers": final_list})
        return resp


class PublishLayers(APIView):
    def get(self, request, format=None):
        return Response()



