from django.urls import path
from .views import DiagramsHome

app_name = 'diagrams'
urlpatterns = [
    path('', DiagramsHome.as_view(), name='index'),
    path('collector', DiagramsHome.as_view(template="diagrams/CollectorProjectGuide.html"), name='collector')
]



