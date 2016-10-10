from django.contrib.auth.models import User
from .test_models import *
from .test_serializers import *
from .test_views import *
from django.test import Client

try:
    user = User.objects.create_user(username="tester",
                                    email="richardh522@gmail.com",
                                    password="test")
    user.save()

except:
    pass

c = Client()
c.login(username='tester', password='test')
