from rest_framework import routers
from .views import OnlineViewSet, FClassViewSet, PLogViewSet

app_name = 'cloudSync'
router = routers.DefaultRouter()
router.register(r'local', FClassViewSet)
router.register(r'web', OnlineViewSet)
router.register(r'publisher', PLogViewSet)

urlpatterns = []

urlpatterns += router.urls


