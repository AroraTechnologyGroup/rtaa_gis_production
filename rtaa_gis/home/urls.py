from django.conf.urls import include, url
from django.contrib.auth.views import logout, login, password_change
from .views import HomePage

app_name = 'home'
urlpatterns = [
    url(r'^$', HomePage.as_view(), name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': 'home:login'}, name='logout'),
    url(r'^password_change/$', password_change, {'next': '/'}, name='password_change')
]



