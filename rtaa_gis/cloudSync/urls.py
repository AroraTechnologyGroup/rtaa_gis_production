from .views import ViewLayers, PublishLayers
from django.conf.urls import url

app_name = 'cloudSync'
urlpatterns = [
    url(r'^viewer/$', ViewLayers.as_view()),
    url(r'^publisher/$', PublishLayers.as_view())
]

