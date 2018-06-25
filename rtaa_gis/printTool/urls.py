from . import views
from django.urls import path

app_name = 'printTool'
urlpatterns = [
    path('layout', views.layout),
    path('agol_user', views.agol_user),
    path('graphics', views.parseGraphics),
    path('list', views.getPrintList),
    path('delete', views.delete_file),
    path('markups', views.getMarkupList),
    path('email', views.emailExhibit)
]

