from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
from .utils.ldap_tool import LDAPQuery
from django.contrib.auth.models import User, Group
import logging

logger = logging.getLogger(__package__)


# Create your views here.
class HomePage(APIView):
    """View that renders the opening homepage"""
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (AllowAny,)
    template = r'home/main_content/main_content.html'

    def get(self, request, format=None):
        if not request.user.is_authenticated():
            return redirect(reverse('home:login'))
        name = request.user.username
        resp = Response(template_name=self.template)
        resp['Cache-Control'] = 'no-cache'
        query = LDAPQuery(name, 'gisapps.aroraengineers.com')
        groups = query.get_groups()
        logger.info(groups)
        user_obj = User.objects.get(username=name)
        
        users_groups = user_obj.groups.all()
        for x in users_groups:
            if x not in groups:
                try:
                    g = Group.objects.get(name=x)
                    user_obj.groups.remove(g)
                    user_obj.save()
                except:
                    pass

        for x in groups:
            if x not in users_groups:
                try:
                    g = Group.objects.get(name=x)
                    user_obj.groups.add(g)
                    user_obj.save()
                except:
                    pass
        return resp

