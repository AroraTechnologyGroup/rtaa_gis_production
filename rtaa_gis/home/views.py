from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.template.response import TemplateResponse
from rest_framework.response import Response
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
from .utils.ldap_tool import LDAPQuery
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
import logging
from datetime import datetime
from rest_framework_jsonp.renderers import JSONRenderer
import os
from django.conf import settings
from django.views.decorators.cache import never_cache
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


logger = logging.getLogger(__package__)

schema_view = get_schema_view(title='RTAA API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


def query_ldap(name):
    """this functions is used in the api function view and the HomePage View Class"""
    # Perform inheritance from AD
    local_name = name.split("\\")[-1]
    if settings.LDAP_URL == "renoairport.net":
        if settings.DEBUG:
            local_name = "AroraTeam"

    query = LDAPQuery(local_name, settings.LDAP_URL)
    ldap_groups = query.get_groups()
    logger.info("ldap_groups = {}".format(ldap_groups))
    logger.info("username = {}".format(local_name))

    user_obj = User.objects.get(username=name)
    users_groups = user_obj.groups.all()
    # remove groups from user if not in LDAP group list
    for x in users_groups:
        if x.name not in ldap_groups:
            try:
                # g = Group.objects.get(name=x)
                user_obj.groups.remove(x)
                # user_obj.save()
            except Exception as e:
                print(e)
    # add user to group if group exists in ldap and local group table
    for x in ldap_groups:
        if x not in [g.name for g in users_groups]:
            try:
                g = Group.objects.get(name=x)
                # g = Group.objects.get(name="tester")
                user_obj.groups.add(g)
                # user_obj.save()
            except Exception as e:
                print(e)
    groups = [x.name for x in user_obj.groups.all()]
    data = {
        "user": local_name,
        "groups": groups
    }
    return data


def get_name(request):
    """from the request return the domain username or the local user for testing"""
    try:
        name = request.META['REMOTE_USER']
        logger.info("Remote username = {}".format(name))
    except KeyError:
        name = request.user.username
        logger.info("non-Remote username = {}".format(name))
    # for testing, if username is '', set it to superuser from django admin
    if name == '':
        name = 'siteadmin'
    return name


@api_view(['GET'])
def build_groups(request, format=None):
    """View to inherit from AD and build the app tables"""
    name = get_name(request)
    user_data = query_ldap(name)
    return Response(user_data)


@api_view(['GET'])
def user_groups(request, format=None):
    """View to get the user's groups from the framework tables"""
    name = get_name(request)
    local_name = name.split("\\")[-1]
    user_obj = User.objects.get(username=name)
    users_groups = user_obj.groups.all()
    groups = [x.name for x in users_groups]
    user_data = {
        "user": local_name,
        "groups": groups
    }
    return Response(user_data)


@api_view(['GET', 'POST'])
def clear_users(request, format=None):
    users = User.objects.all()
    removed = []
    for user in users:
        if user.username.split("\\")[0] == "GISAPPS":
            user.delete()
            removed.append(user.username)
    return Response(data="These users were removed :: {} :: {}".format(removed, datetime.now()))


@method_decorator(ensure_csrf_cookie, name="dispatch")
# @method_decorator(never_cache, name="dispatch")
class HomePage(APIView):
    """View that renders the main homepage or an app depending on the template"""
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    permission_classes = (AllowAny,)
    template = r'home/home_body.html'
    app_name = ""

    def get(self, request, format=None):

        if not request.user.is_authenticated():
            return redirect(reverse('home:login'))

        resp = Response(template_name=self.template)
        resp['Cache-Control'] = 'no-cache'

        name = get_name(request)
        # run this function to inherit groups from AD
        final_groups = query_ldap(name)
        final_groups = [x.name for x in final_groups]

        local_name = name.split("\\")[-1]
        # Create user's folder in the media root
        users_dir = os.path.join(settings.MEDIA_ROOT, 'users')
        if not os.path.exists(users_dir):
            os.mkdir(users_dir)
        user_dir = os.path.join(users_dir, local_name)
        if not os.path.exists(user_dir):
            os.mkdir(user_dir)

        # make the print directory for the user
        # TODO - move this to the print App
        print_dir = os.path.join(user_dir, "prints")
        if not os.path.exists(print_dir):
            os.mkdir(print_dir)

        server_url = settings.SERVER_URL
        app_name = self.app_name.strip('/')
        resp.data = {"server_url": server_url, "groups": final_groups, "app_name": app_name}
        return resp