from rest_framework import routers
from . import views
from django.conf.urls import url

router = routers.DefaultRouter()
router.register(r'grids', views.EngGridViewSet)
router.register(r'eng-assignments', views.EngAssignmentViewSet)
router.register(r'eng-all-files', views.EngViewSet)
router.register(r'eng-io', views.EngIOViewSet)
router.register(r'eng-files', views.PagedEngViewSet)


urlpatterns = [
    url(r'swag/', views.schema_view),
]

urlpatterns += router.urls
