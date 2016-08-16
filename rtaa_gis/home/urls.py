from django.conf.urls import include, url
from . import views


urlpatterns = [
    url('^', views.HomePage.as_view()),
]



