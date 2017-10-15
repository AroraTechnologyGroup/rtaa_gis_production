from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
app_name = 'printTool'
urlpatterns = [
    url(r'execute', views.print_agol),
    url(r'list', views.getPrintList),
    url(r'delete', views.delete_file)
]

urlpatterns += router.urls
