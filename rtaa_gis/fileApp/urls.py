from rest_framework import routers
from . import views
from .views import UserViewer, FileUpdater
from django.conf.urls import url

app_name = 'fileApp'

router = routers.DefaultRouter()
router.register(r'grids', views.EngGridViewSet)
router.register(r'eng-assignments', views.EngAssignmentViewSet)
router.register(r'eng-all-files', views.EngViewSet)
router.register(r'eng-io', views.EngIOViewSet)
router.register(r'eng-files', views.PagedEngViewSet)


urlpatterns = [
    url(r'^eDocViewer/$', UserViewer.as_view(template='fileApp/eDocUserView.html', app_name='eDoc Viewer'), name='eDoc'),
    url(r'^file-update/$', FileUpdater.as_view(), name='file-updater')
]

urlpatterns += router.urls
