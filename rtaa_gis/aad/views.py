from xml.dom.minidom import parseString
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from requests_oauthlib import OAuth2Session
from . import oauth
from .serializers import WebApplicationSerializer
from .forms import ContactForm
import arcrest
from arcrest import security
import requests
import json


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            org_url = r"https://aroragis.maps.arcgis.com"
            org_id = r"Apy6bpbM5OoW9DX4"

            # perform the action with the creds here
            service_root = r"https://graph.windows.net"
            tenant_id = r"aroraengineers.com"
            resource_path = "groups"
            query_parameters = "api-version=1.6&format=json"

            # Sample groups returned from AD that match group in AGOL
            groups = ['Reno-Tahoe Share']
            config = {
                'username': username,
                'password': password,
                'org_id': org_id,
                'org_url': org_url
            }

            agol_apps = query_agol(config, groups)

            return HttpResponse(json.dumps(agol_apps), content_type="application/json")
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'aad/index.html', context)


def query_agol(config, groups):
    """groups should be an array of group names from AD that match AGOL
    a dictionary of {app title: app url} is returned"""

    agol = security.AGOLTokenSecurityHandler(
        username=config['username'], password=config['password'],
        org_url=config['org_url']
    )

    admin = arcrest.manageorg.Administration(
        url=config['org_url'], securityHandler=agol
    )

    gr = admin.community.groups.search(
        q="{}".format(groups[0]))

    resp = gr['results'][0]
    data = {
        'id': resp.get('id'),
        'title': resp.get('title')
    }

    items = admin.content.group(data['id']).items
    apps = []
    for x in items:
        if x['type'] == "Web Mapping Application":
            data = {'title': x['title'], 'url': x['url']}
            apps.append(data)
    if len(apps):
        new_data = WebApplicationSerializer(many=True, data=apps)
        if new_data.is_valid():
            return new_data.validated_data
