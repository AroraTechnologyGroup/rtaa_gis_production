from rest_framework import routers
from django.conf.urls import url
from . import views

router = routers.DefaultRouter()
router.register(r'grids', views.GridViewSet)
router.register(r'all-files', views.FileViewSet)
router.register(r'io', views.IOViewSet)
router.register(r'files', views.PagedFileViewSet)
router.register(r'assignments', views.AssignmentViewSet)

urlpatterns = [
    url(r'^dojo-login/$', views.dojo_login),
]

urlpatterns += router.urls
