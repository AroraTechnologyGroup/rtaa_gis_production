from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
urlpatterns = [
    url(r'submitJob', views.print_map),
]

urlpatterns += router.urls
