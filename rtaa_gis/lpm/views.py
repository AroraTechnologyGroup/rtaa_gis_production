import os
import sys
import logging
import traceback
from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import AgreementSerializer
from .models import Agreement


logger = logging.getLogger(__name__)


def log_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    return repr(traceback.format_exception(exc_type, exc_value, exc_traceback))


@method_decorator(ensure_csrf_cookie, name='dispatch')
class AgreementViewSet(viewsets.ModelViewSet):
    """Active agreements from ABM"""
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer



