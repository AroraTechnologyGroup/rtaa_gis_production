from django.conf.urls import url
from . import views

urlpatterns = [
    url('^', views.MatchNames.as_view()),
    url('^upload/(?P<filename>[^/]+)$', views.UploadFile.as_view())
]
