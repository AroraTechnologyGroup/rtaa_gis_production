from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
import logging


logger = logging.getLogger(__package__)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class DiagramsHome(APIView):
    """View that renders the main homepage or an app depending on the template"""
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (AllowAny,)
    template = r'diagrams/diagrams_body.html'

    def get(self, request, format=None):

        if not request.user.is_authenticated():
            return redirect(reverse('home:login'))

        resp = Response(template_name=self.template)
        return resp
