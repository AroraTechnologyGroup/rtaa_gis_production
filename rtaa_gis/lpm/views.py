import os
import sys
import logging
import traceback

from rest_framework.decorators import api_view, renderer_classes

from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import detail_route

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import AgreementSerializer, SpaceSerializer
from .models import Agreement, Space

MEDIA_ROOT = settings.MEDIA_ROOT
BASE_DIR = settings.BASE_DIR
LOGIN_URL = settings.LOGIN_URL
LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
FILE_APP_TOP_DIRS = settings.FILE_APP_TOP_DIRS

logger = logging.getLogger(__name__)


def log_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return repr(traceback.format_exception(exc_type, exc_value, exc_traceback))


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AgreementViewSet(viewsets.ModelViewSet):
    """Active agreements from ABM"""
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SpaceViewSet(viewsets.ModelViewSet):
    """Space from the GIS, related to agreements"""
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SpaceEditor(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'space_editor.html'

    @detail_route(methods=['get',])
    def get(self, request, id, format=None):
        space = get_object_or_404(Space, id=id)
        serializer = SpaceSerializer(space)
        return Response({'serializer': serializer, 'space': space})

    @detail_route(methods=['post',])
    def post(self, request, id, format=None):
        space = get_object_or_404(Space, id=id)
        serializer = SpaceSerializer(space, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'space': space})
        serializer.save()
        return Response({'serializer': serializer, 'space': space})
