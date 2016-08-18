from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, views
from django.urls import reverse


# Create your views here.
class HomePage(APIView):
    """View that renders the opening homepage"""
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (AllowAny,)
    template = r'home/main_content.html'

    def post(self, request):
        if not request.user.is_authenticated():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home:process'))

    def get(self, request):
        if not request.user.is_authenticated():
            return redirect(reverse('home:login'), next='')
        context = {"data": []}
        return Response(context, template_name=self.template)



