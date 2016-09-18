from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, views
from django.urls import reverse
from utils import deploy
from rtaa_gis.settings import BASE_DIR
import os
import json


# Create your views here.
class HomePage(APIView):
    """View that renders the opening homepage"""
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (AllowAny,)
    template = r'home/main_content/main_content.html'

    def get(self, request, format=None):
        if not request.user.is_authenticated():
            return redirect(reverse('home:login'))
        resp = Response(template_name=self.template)
        resp['Cache-Control'] = 'no-cache'
        return resp


class GitPull(APIView):
    """View that calls git pull on the repo"""
    renderer_classes = (JSONRenderer,)
    permission_classes = (AllowAny,)

    def get(self, request):
        staging_path = os.path.dirname(BASE_DIR)
        x = deploy.pull(staging_path)
        return Response(json.dumps(x))
