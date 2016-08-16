from rest_framework import routers
from django.conf.urls import include, url
from . import views

router = routers.DefaultRouter()
router.register('grids', views.GridViewSet)
router.register('all-files', views.FileViewSet)
router.register('io', views.IOViewSet)
router.register('files', views.PagedFileViewSet)
router.register('assignments', views.AssignmentViewSet)

urlpatterns = [
    url('^dojo-login/$', views.dojo_login),
    url('^login/$', views.api_login),
    url('^', include('django.contrib.auth.urls'))
]

urlpatterns += router.urls
