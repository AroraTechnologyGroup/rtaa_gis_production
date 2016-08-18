from django.conf.urls import include, url
from django.contrib.auth.views import logout_then_login, login, password_change
from .views import HomePage

app_name = 'home'
urlpatterns = [
    url(r'^$', HomePage.process),
    url(r'login/$', login, name='login'),
    url(r'logout/$', logout_then_login, name='logout'),
    url(r'password_change/$', password_change, {'next': '/'}, name='password_change')
]



