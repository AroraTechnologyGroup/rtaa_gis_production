from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^', views.MatchNames.as_view()),
    url(r'^upload/(?P<filename>[^/]+)$', views.UploadFile.as_view())
]
