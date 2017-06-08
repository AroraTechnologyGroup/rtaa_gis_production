from django.shortcuts import render
from rest_framework_jsonp.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import logging
from datetime import datetime
import os
from django.conf import settings
from django.views.decorators.cache import never_cache

logger = logging.getLogger(__package__)


@method_decorator(ensure_csrf_cookie, name="dispatch")
@method_decorator(never_cache, name='dispatch')
class GISAdmin(APIView):
    """View that renders the GIS Admin Site Analytics Page"""
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (AllowAny,)
    template = r'analytics/gisAdmin.html'

    def get(self, request, format=None):

        if not request.user.is_authenticated():
            return redirect(reverse('home:login'))
        try:
            name = request.META['REMOTE_USER']
        except KeyError:
            name = request.user.username

        resp = Response(template_name=self.template)
        resp['Cache-Control'] = 'no-cache'
        return resp
