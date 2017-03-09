from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
urlpatterns = [
    url(r'execute', views.print_mxdx),
    url(r'delete', views.delete_file)
]

urlpatterns += router.urls
