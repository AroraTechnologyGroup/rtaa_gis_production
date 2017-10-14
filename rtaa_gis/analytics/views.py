import logging
from .serializers import RecordSerializer
from .models import Record

from rest_framework import viewsets
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

logger = logging.getLogger(__package__)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class RecordViewSet(viewsets.ModelViewSet):
    serializer_class = RecordSerializer
    queryset = Record.objects.all()
