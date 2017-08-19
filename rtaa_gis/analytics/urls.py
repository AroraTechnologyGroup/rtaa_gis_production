from rest_framework import routers
from .views import GISAdmin
from django.conf.urls import url

router = routers.DefaultRouter()
app_name = 'analytics'
urlpatterns = [
    url(r'^$', GISAdmin.as_view(), name='gis-admin')
]
urlpatterns += router.urls