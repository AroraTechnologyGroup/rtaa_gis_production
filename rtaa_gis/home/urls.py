from django.conf.urls import url
from django.contrib.auth.views import logout, login, password_change
from .views import HomePage, user_groups, clear_users, schema_view

app_name = 'home'
urlpatterns = [
    url(r'^$', HomePage.as_view(), name='index'),
    url(r'^docs', schema_view, name="docs"),
    url(r'^groups/$', user_groups),
    url(r'^login/$', login, {'extra_context': {'next': '/#home'}}, name='login'),
    url(r'^logout/$', logout, {'next_page': 'home:login'}, name='logout'),
    url(r'^clear/$', clear_users),

    # These urls for web mapping applications are also specified in the application_cards.json file, loaded
    # with the static files for the home app, as the value for the 'path' key.
    # The app_name corresponds to the application on IIS that gets loaded in the iframe
    url(r'^viewer/$', HomePage.as_view(template='home/AppLoader.html', app_name='gisviewer'), name='viewer'),
    url(r'^airspace/$', HomePage.as_view(template='home/AppLoader.html', app_name='airspace_restricted'),
        name='airspace'),
    url(r'^leaseProperty/$', HomePage.as_view(template='home/AppLoader.html', app_name='rtaa_lpm'),
        name='leaseProperty'),
    url(r'^signageMarking/$', HomePage.as_view(template='home/AppLoader.html', app_name='Signs'),
        name='signageMarking'),
    url(r'^mobile/$', HomePage.as_view(template='home/AppLoader.html', app_name='gisviewer'), name='mobile'),
    # url(r'^password_change/$', password_change, {'post_change_redirect': 'home:login'}, name='password_change')
]



