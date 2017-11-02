import os
import sys
import logging
import traceback

from rest_framework.decorators import api_view, renderer_classes

from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework import viewsets
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import AgreementSerializer
from .models import Agreement
MEDIA_ROOT = settings.MEDIA_ROOT
BASE_DIR = settings.BASE_DIR
LOGIN_URL = settings.LOGIN_URL
LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL
FILE_APP_TOP_DIRS = settings.FILE_APP_TOP_DIRS

logger = logging.getLogger(__name__)


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='eDoc API')
    return response.Response(generator.get_schema(request=request))


def log_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return repr(traceback.format_exception(exc_type, exc_value, exc_traceback))


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AgreementViewSet(viewsets.ModelViewSet):
    """Grid Cells within the ArcGIS Online Map Grid"""
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer

