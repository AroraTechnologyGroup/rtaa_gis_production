from . import views
from django.urls import path

app_name = 'printTool'
urlpatterns = [
    path('layout', views.layout),
    path('graphics', views.parseGraphics),
    path('list', views.getPrintList),
    path('delete', views.delete_file),
    path('markups', views.getMarkupList),
    path('email', views.emailExhibit)
]

