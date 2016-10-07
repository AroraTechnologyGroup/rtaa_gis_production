from django.test import Client
from django.contrib.auth.models import User

try:
    user = User.objects.create_user(username="tester",
                                    email="richardh522@gmail.com",
                                    password="test")
    user.save()

except:
    pass

c = Client()
c.login(username='tester', password='test')
