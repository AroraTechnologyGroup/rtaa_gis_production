from django.conf.urls import url
from .views import DiagramsHome

app_name = 'diagrams'
urlpatterns = [
    url(r'^$', DiagramsHome.as_view(), name='index'),
    url(r'^collector/', DiagramsHome.as_view(template="diagrams/CollectorProjectGuide.html"), name='collector')
]



