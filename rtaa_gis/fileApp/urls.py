from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'assignments', views.AssignmentViewSet)
router.register(r'grids', views.GridViewSet)
router.register(r'all-files', views.FileViewSet)
router.register(r'io', views.IOViewSet)
router.register(r'files', views.PagedFileViewSet)


urlpatterns = [
    url(r'swag/', views.schema_view),
]

urlpatterns += router.urls
