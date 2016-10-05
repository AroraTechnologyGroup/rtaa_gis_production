from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny


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

