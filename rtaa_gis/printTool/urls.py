from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
urlpatterns = [
    url(r'execute', views.print_map),
    url(r'delete', views.delete_file)
]

urlpatterns += router.urls
